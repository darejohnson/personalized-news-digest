# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (Docker layer caching optimization)
COPY requirements/ ./requirements/

# Install dependencies
RUN pip install --no-cache-dir -r requirements/base.txt

# Copy application code
COPY src/ ./src/
COPY .env ./

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]