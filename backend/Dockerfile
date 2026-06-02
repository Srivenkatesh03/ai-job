# Stage 1: Build stage
FROM python:3.11-slim AS builder

WORKDIR /build

# Install compilation build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies to a local folder
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.11-slim AS runtime

WORKDIR /workspace

# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Create non-root user for security compliance
RUN groupadd -g 1000 appgroup && \
    useradd -r -u 1000 -g appgroup appuser

# Copy application files with ownership
COPY --chown=appuser:appgroup app /workspace/app
COPY --chown=appuser:appgroup .env /workspace/.env

# Use non-root user
USER appuser

EXPOSE 8000

# Default command runs FastAPI app; can be overridden in docker-compose for workers
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
