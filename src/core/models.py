from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# First, model what the API actually returns
class NewsAPISource(BaseModel):
    id: Optional[str] = None
    name: str

class NewsAPIArticle(BaseModel):
    source: NewsAPISource
    author: Optional[str] = None
    title: str
    description: Optional[str] = None
    url: str
    urlToImage: Optional[str] = None
    publishedAt: Optional[str] = None
    content: Optional[str] = None

class NewsAPIResponse(BaseModel):
    status: str
    totalResults: int
    articles: List[NewsAPIArticle]

# Now, our internal clean model
class Article(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: str
    source: str  # We'll extract just the source name
    published_at: Optional[datetime] = None
    raw_data: Optional[Dict[str, Any]] = None  # Keep original for debugging

    @classmethod
    def from_newsapi(cls, api_article: NewsAPIArticle) -> 'Article':
        """Transform NewsAPI response to our clean internal format"""
        return cls(
            title=api_article.title,
            description=api_article.description,
            content=api_article.content,
            url=api_article.url,
            source=api_article.source.name,  # Extract just the name
            published_at=api_article.publishedAt,
            raw_data=api_article.dict()  # Keep original for reference
        )