# Personalized News Digest

An AI-powered agent that fetches news articles based on user preferences and summarizes them in a digest format.

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file and set `NEWS_API_KEY` and `OPENAI_API_KEY`.
5. Run the app: `uvicorn src.main:app --reload`

## Usage



# 🧠 AI-Powered News Digest

A production-ready full-stack application that fetches, summarizes, and delivers personalized news using cutting-edge LLM engineering patterns.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)

## 🎯 Overview

This isn't just another "hello world" AI project. It's a **production-grade system** that demonstrates professional software engineering practices applied to LLM applications. The system intelligently fetches news articles, summarizes them using OpenAI GPT, and presents them through a clean web interface - all while managing costs, handling errors gracefully, and maintaining scalability.

## 🚀 Features

### 🤖 AI & ML Capabilities
- **Smart Summarization**: GPT-powered article summarization with prompt engineering
- **Cost Optimization**: Token tracking and budget enforcement to prevent overspending
- **Quality Filtering**: Intelligent content screening to avoid summarizing low-quality articles

### 🛠️ Engineering Excellence
- **Production Resilience**: Circuit breakers, exponential backoff retry logic, and graceful degradation
- **Real-time Monitoring**: Comprehensive health checks, cost metrics, and system status endpoints
- **Containerized Deployment**: Full Docker support for consistent development and production environments
- **API-First Design**: Clean RESTful API with proper error handling and documentation

### 📊 User Experience
- **Streamlit Web Interface**: Intuitive UI for non-technical users
- **Personalized Digests**: Topic-based news filtering and summarization
- **Cost Transparency**: Real-time spending tracking and budget awareness

## 🏗️ Architecture

```text
personalized-news-digest/
├── 🐳 docker-compose.yml # Multi-container orchestration
├── ⚙️ Dockerfile # Backend container blueprint
├── 🎨 Dockerfile.streamlit # Frontend container blueprint
├── 📁 src/
│ ├── 🏗️ main.py # FastAPI application entry point
│ ├── 🔧 config/settings.py # Configuration management
│ └── 💼 core/ # Business logic layer
│ ├── models.py # Data models with Pydantic
│ ├── news_fetcher.py # NewsAPI integration with caching
│ ├── summarizer.py # OpenAI integration with cost control
│ ├── cost_controller.py # Budget management and tracking
│ └── api_resilience.py # Retry logic and circuit breakers
├── 📋 requirements/ # Dependency management
└── 🖥️ app.py # Streamlit frontend application
```

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | FastAPI, Uvicorn | High-performance API server |
| **AI/ML** | OpenAI GPT, NewsAPI | Content summarization and news sourcing |
| **Frontend** | Streamlit | Interactive web interface |
| **Infrastructure** | Docker, Docker Compose | Containerization and orchestration |
| **Monitoring** | Custom metrics, Health checks | System observability |
| **Data Validation** | Pydantic | Runtime type checking and validation |

## 🏃‍♂️ Quick Start

### Prerequisites
- Docker and Docker Compose
- NewsAPI key (free at [newsapi.org](https://newsapi.org))
- OpenAI API key (from [OpenAI Platform](https://platform.openai.com))

### One-Command Deployment
```bash
# Clone the repository
git clone https://github.com/yourusername/personalized-news-digest
cd personalized-news-digest

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Launch the entire application
docker-compose up --build

Access Points
🌐 Web Interface: http://localhost:8501

🔗 API Documentation: http://localhost:8000/docs

❤️ Health Check: http://localhost:8000/health

📊 System Metrics: http://localhost:8000/system-status

📚 API Reference

Core Endpoints
Endpoint	    | Method | Description
/news/{topic}	| GET	| Fetch and summarize news for a topic
/health	        | GET	| Basic service health check
/system-status	| GET	| Comprehensive system metrics
/cost-metrics	| GET	| Real-time cost tracking


Example Usage
# Get summarized news about AI
curl "http://localhost:8000/news/artificial%20intelligence"

# Check system health
curl "http://localhost:8000/health"

# Monitor costs
curl "http://localhost:8000/cost-metrics"


🎓 Learning Outcomes
This project demonstrates professional software engineering practices in the context of LLM applications:

🔧 Technical Skills
LLM Integration: Professional OpenAI API usage with cost control

API Design: RESTful principles with proper error handling

Containerization: Docker and multi-service orchestration

System Design: Microservices architecture with clear separation of concerns

Production Readiness: Monitoring, resilience, and scalability patterns

💡 Engineering Concepts
Circuit Breaker Pattern: Preventing cascade failures

Exponential Backoff: Intelligent retry mechanisms

Cost Optimization: Token management and budget enforcement

Graceful Degradation: Maintaining service during partial failures

Configuration Management: Environment-based settings with validation

🚀 Deployment
Local Development

# Without Docker (for development)
pip install -r requirements/base.txt
uvicorn src.main:app --reload
streamlit run app.py


Production Deployment
# Using Docker Compose
docker-compose -f docker-compose.yml up -d

# Using individual containers
docker build -t news-backend -f Dockerfile .
docker build -t news-frontend -f Dockerfile.streamlit .


🔍 Monitoring & Observability
The application includes comprehensive monitoring:

Health Checks: Automated service availability monitoring

Cost Tracking: Real-time OpenAI API spending

Performance Metrics: Response times and error rates

Circuit Breaker Status: Resilience pattern monitoring


🤝 Contributing
This project welcomes contributions! Please feel free to:

Report bugs and issues

Suggest new features

Submit pull requests

Improve documentation

📄 License
This project is open source and available under the GNU General Public License v3.0 