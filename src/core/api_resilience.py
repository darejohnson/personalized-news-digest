import logging
import time
from typing import Optional, Callable, Any
from functools import wraps
from openai import RateLimitError, APIError

logger = logging.getLogger(__name__)

class ResilienceManager:
    """
    Handles API rate limits, retries, and circuit breaking
    """
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.circuit_open = False
        self.circuit_last_failure_time = 0
        self.circuit_timeout = 60  # 60 seconds circuit breaker
    
    def execute_with_retry(self, api_call: Callable) -> Any:
        """
        Execute an API call with retry logic and circuit breaker
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                # Check circuit breaker first
                if self.circuit_open:
                    if time.time() - self.circuit_last_failure_time < self.circuit_timeout:
                        logger.warning("Circuit breaker open - skipping request")
                        return None
                    else:
                        logger.info("Circuit breaker reset - trying again")
                        self.circuit_open = False
                
                # Try the actual API call
                result = api_call()
                
                # If successful, reset circuit breaker
                if self.circuit_open:
                    logger.info("Circuit breaker closed - requests succeeding again")
                    self.circuit_open = False
                
                return result
                
            except RateLimitError as e:
                last_exception = e
                wait_time = self.base_delay * (2 ** attempt)  # Exponential backoff
                logger.warning(f"Rate limit hit, attempt {attempt + 1}/{self.max_retries + 1}. Waiting {wait_time}s")
                time.sleep(wait_time)
                
            except APIError as e:
                last_exception = e
                if e.status_code >= 500:  # Server errors - retry
                    wait_time = self.base_delay * (2 ** attempt)
                    logger.warning(f"API server error {e.status_code}, retrying in {wait_time}s")
                    time.sleep(wait_time)
                else:  # Client errors - don't retry
                    logger.error(f"API client error {e.status_code}: {e.message}")
                    break
                    
            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected error on attempt {attempt + 1}: {str(e)}")
                break
        
        # If we exhausted all retries, open circuit breaker
        if attempt == self.max_retries and last_exception:
            logger.error(f"All {self.max_retries} retries failed. Opening circuit breaker.")
            self.circuit_open = True
            self.circuit_last_failure_time = time.time()
        
        return None
    
    def get_circuit_status(self) -> dict:
        """Get current circuit breaker status"""
        return {
            "circuit_open": self.circuit_open,
            "last_failure_time": self.circuit_last_failure_time,
            "time_since_last_failure": time.time() - self.circuit_last_failure_time if self.circuit_last_failure_time else None
        }