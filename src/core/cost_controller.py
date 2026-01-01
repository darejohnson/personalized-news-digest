import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from src.core.models import Article

logger = logging.getLogger(__name__)

class CostController:
    """
    Prevents budget overruns and optimizes API usage
    """
    
    def __init__(self, daily_budget: float = 1.0):  # $1.00 daily budget
        self.daily_budget = daily_budget
        self.daily_spent: float = 0.0
        self.reset_time = datetime.now()
        self.processed_urls: set = set()  # Track already processed articles
        
        # Cost per 1K tokens for gpt-3.5-turbo (approx)
        self.input_cost_per_1k = 0.0015  # $0.0015 per 1K input tokens
        self.output_cost_per_1k = 0.0020  # $0.0020 per 1K output tokens
    
    def should_process_article(self, article: Article) -> bool:
        """
        Decision engine: Should we spend money summarizing this article?
        """
        # Check 1: Have we already processed this URL?
        if article.url in self.processed_urls:
            logger.info(f"Skipping duplicate article: {article.title[:50]}...")
            return False
        
        # Check 2: Are we over daily budget?
        if self.daily_spent >= self.daily_budget:
            logger.warning(f"Daily budget exceeded: ${self.daily_spent:.4f}/{self.daily_budget}")
            return False
        
        # Check 3: Is this article worth summarizing?
        if not self._is_article_quality(article):
            logger.info(f"Skipping low-quality article: {article.title[:50]}...")
            return False
        
        # Check 4: Reset daily spending if it's a new day
        self._reset_if_new_day()
        
        return True
    
    def _is_article_quality(self, article: Article) -> bool:
        """
        Basic quality checks to avoid wasting money on junk
        """
        # Minimum content length
        min_content_length = 200
        content = article.content or article.description or ""
        
        if len(content) < min_content_length:
            return False
        
        # Check for clickbait patterns (very basic)
        clickbait_indicators = ["SHOCKING", "YOU WON'T BELIEVE", "GURU", "SECRET"]
        title_upper = article.title.upper()
        
        if any(indicator in title_upper for indicator in clickbait_indicators):
            return False
            
        return True
    
    def record_usage(self, prompt_tokens: int, completion_tokens: int):
        """
        Track token usage and calculate cost
        """
        prompt_cost = (prompt_tokens / 1000) * self.input_cost_per_1k
        completion_cost = (completion_tokens / 1000) * self.output_cost_per_1k
        total_cost = prompt_cost + completion_cost
        
        self.daily_spent += total_cost
        self._reset_if_new_day()
        
        logger.info(f"API Cost: ${total_cost:.6f} (Prompt: {prompt_tokens}, Completion: {completion_tokens})")
        logger.info(f"Daily total: ${self.daily_spent:.4f}/{self.daily_budget}")
    
    def _reset_if_new_day(self):
        """Reset daily spending at midnight"""
        now = datetime.now()
        if now.date() > self.reset_time.date():
            self.daily_spent = 0.0
            self.reset_time = now
            self.processed_urls.clear()  # Clear cache daily
            logger.info("Daily budget reset")
    
    def get_cost_metrics(self) -> Dict:
        """Get current cost metrics for monitoring"""
        return {
            "daily_spent": round(self.daily_spent, 4),
            "daily_budget": self.daily_budget,
            "remaining_budget": round(self.daily_budget - self.daily_spent, 4),
            "reset_time": self.reset_time.isoformat()
        }