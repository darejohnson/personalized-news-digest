import threading
import time
from typing import Optional, Dict, Tuple

class TTLCache:
    def __init__(self, ttl_seconds: int = 24 * 60 * 60):  # default 24 hours
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Tuple[float, str]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[str]:
        with self._lock:
            if key in self._cache:
                timestamp, value = self._cache[key]
                if time.time() - timestamp < self.ttl_seconds:
                    return value
                else:
                    del self._cache[key]
            return None

    def set(self, key: str, value: str) -> None:
        with self._lock:
            self._cache[key] = (time.time(), value)

    def clear_expired(self) -> None:
        with self._lock:
            current_time = time.time()
            expired_keys = [key for key, (ts, _) in self._cache.items() if current_time - ts >= self.ttl_seconds]
            for key in expired_keys:
                del self._cache[key]