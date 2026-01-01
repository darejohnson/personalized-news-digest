import logging
from typing import Optional
from openai import OpenAI
from src.core.models import Article
from src.config.settings import settings
from src.core.cost_controller import CostController
from src.core.api_resilience import ResilienceManager
from src.core.cache import TTLCache

logger = logging.getLogger(__name__)

class SmartSummarizer:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.max_tokens = settings.max_tokens
        self.cost_controller = CostController()
        self.resilience = ResilienceManager()
        self.cache = TTLCache(ttl_seconds=604800)  # 7 days
        
    def summarize_article(self, article: Article) -> Optional[str]:
        # First, check the cache
        cached_summary = self.cache.get(article.url)
        if cached_summary is not None:
            logger.info(f"Cache hit for article: {article.title[:50]}...")
            return cached_summary

        """
        Enhanced summarization with cost control, quality checks, AND resilience
        """
        # Cost control decision
        if not self.cost_controller.should_process_article(article):
            return None
            
        try:
            content = self._prepare_content(article)
            prompt = self._build_summarization_prompt(content)
            
            logger.info(f"Summarizing article: {article.title[:50]}...")
            
            # Use the resilience manager to execute with retry logic
            def make_api_call():
                return self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system", 
                            "content": self._get_system_prompt()
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    max_tokens=self.max_tokens,
                    temperature=0.3
                )
            
            response = self.resilience.execute_with_retry(make_api_call)
            
            if response is None:  # All retries failed
                return None
                
            summary = response.choices[0].message.content.strip()



            if summary is not None:
                self.cache.set(article.url, summary)


            
            # Record cost for this request
            if response.usage:
                self.cost_controller.record_usage(
                    response.usage.prompt_tokens,
                    response.usage.completion_tokens
                )
            
            # Mark as processed
            self.cost_controller.processed_urls.add(article.url)
            
            return summary
            
        except Exception as e:
            logger.error(f"Summarization failed for '{article.title}': {str(e)}")
            return None
    
    def _get_system_prompt(self) -> str:
        """More sophisticated system prompt"""
        return """You are a professional news summarizer. Create concise 2-3 sentence summaries that:
        - Capture the main facts and key points
        - Maintain neutral, objective tone
        - Highlight significance or implications
        - Avoid editorializing or adding opinions
        - Use clear, accessible language"""
    
    def _prepare_content(self, article: Article) -> str:
        """Smarter content preparation"""
        content_parts = []
        
        if article.title:
            content_parts.append(f"TITLE: {article.title}")
        if article.description:
            content_parts.append(f"DESCRIPTION: {article.description}")
        if article.content:
            # Smarter truncation - preserve sentences
            content = self._truncate_preserving_sentences(article.content, 2500)
            content_parts.append(f"CONTENT: {content}")
        
        return "\n\n".join(content_parts)
    
    def _truncate_preserving_sentences(self, text: str, max_chars: int) -> str:
        """Truncate text while preserving sentence boundaries"""
        if len(text) <= max_chars:
            return text
            
        # Find the last sentence end before max_chars
        truncated = text[:max_chars]
        last_period = truncated.rfind('.')
        last_question = truncated.rfind('?')
        last_exclamation = truncated.rfind('!')
        
        sentence_end = max(last_period, last_question, last_exclamation)
        
        if sentence_end > 0:
            return text[:sentence_end + 1] + ".."
        else:
            return truncated + "..."
    
    def _build_summarization_prompt(self, content: str) -> str:
        """More sophisticated prompt engineering"""
        return f"""
        Please analyze the following news content and provide a concise 2-3 sentence summary.
        
        Focus on:
        - The main event or discovery
        - Key facts and figures  
        - Potential impact or significance
        - Any notable quotes or statements
        
        Write in clear, neutral journalistic style.
        
        CONTENT:
        {content}
        
        SUMMARY:
        """
    
    def get_cost_metrics(self):
        """Expose cost metrics for monitoring"""
        return self.cost_controller.get_cost_metrics()
    
    def get_resilience_metrics(self):
        """Get resilience metrics for monitoring"""
        return self.resilience.get_circuit_status()