from fastapi import FastAPI
from datetime import datetime
from src.core.news_fetcher import NewsFetcher
from src.core.summarizer import SmartSummarizer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Personalized News Digest")

# Initialize components
news_fetcher = NewsFetcher()
summarizer = SmartSummarizer()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "News Digest API is running"}

@app.get("/news/{topic}")
async def get_news(topic: str):
    """
    Enhanced endpoint with cost control and quality filtering
    """
    articles = news_fetcher.fetch_articles(topic)
    
    summarized_articles = []
    skipped_count = 0
    
    for article in articles:
        summary = summarizer.summarize_article(article)
        
        if summary:
            article_dict = article.dict()
            article_dict["ai_summary"] = summary
            summarized_articles.append(article_dict)
        else:
            skipped_count += 1  # Track skipped articles
    
    cost_metrics = summarizer.get_cost_metrics()
    
    return {
        "topic": topic,
        "article_count": len(articles),
        "summarized_count": len(summarized_articles),
        "skipped_count": skipped_count,  # Articles skipped due to cost/quality
        "cost_metrics": cost_metrics,
        "articles": summarized_articles
    }

@app.get("/cost-metrics")
async def get_cost_metrics():
    """Monitor our API spending"""
    return {
        **summarizer.get_cost_metrics(),
        "resilience": summarizer.get_resilience_metrics()
    }

@app.get("/system-status")
async def get_system_status():
    """Comprehensive system health and metrics"""
    cost_metrics = summarizer.get_cost_metrics()
    resilience_metrics = summarizer.get_resilience_metrics()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cost_metrics": cost_metrics,
        "resilience_metrics": resilience_metrics,
        "version": "1.0.0"
    }