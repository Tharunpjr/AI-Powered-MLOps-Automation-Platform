# AutoOps Model Service Dockerfile
# Multi-stage build for optimized production image

# Build stage
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create non-root user
RUN groupadd -r autoops && useradd -r -g autoops autoops

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /home/autoops/.local

# Copy application code
COPY app/ ./app/
COPY models/ ./models/

# Create models directory if it doesn't exist
RUN mkdir -p /app/models

# Set environment variables
ENV PATH=/home/autoops/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV MODEL_PATH=/app/models/model.pkl
ENV LOG_LEVEL=INFO

# Change ownership to non-root user
RUN chown -R autoops:autoops /app

# Switch to non-root user
USER autoops

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
