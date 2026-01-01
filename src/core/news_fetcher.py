import requests
import logging
from typing import List
from src.core.models import NewsAPIResponse, Article
from src.config.settings import settings

logger = logging.getLogger(__name__)

class NewsFetcher:
    def __init__(self):
        self.api_key = settings.newsapi_key
        self.base_url = settings.newsapi_base_url
        
    def fetch_articles(self, topic: str) -> List[Article]:
        """
        Fetch articles from NewsAPI and transform to our internal format
        """
        try:
            url = f"{self.base_url}/everything"
            params = {
                "q": topic,
                "apiKey": self.api_key,
                "pageSize": 10,
                "sortBy": "publishedAt",
                "language": "en"  # Added for consistency
            }
            
            logger.info(f"Fetching news for topic: {topic}")
            
            response = requests.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            
            # Parse using the correct API model
            news_data = NewsAPIResponse(**response.json())
            
            # Transform to our clean internal format
            articles = [
                Article.from_newsapi(api_article) 
                for api_article in news_data.articles
            ]
            
            logger.info(f"Successfully fetched and transformed {len(articles)} articles")
            return articles
            
        except requests.exceptions.Timeout:
            logger.error(f"NewsAPI request timed out for topic: {topic}")
            return []
        except requests.exceptions.HTTPError as e:
            logger.error(f"NewsAPI HTTP error: {e.response.status_code}")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"NewsAPI request failed: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in NewsFetcher: {str(e)}")
            return []