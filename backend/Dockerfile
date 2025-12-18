FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY uv.lock uv.lock
COPY pyproject.toml pyproject.toml

RUN uv sync \
    --frozen \
    --no-dev \

# Copy shared directory (needed by backend)
COPY shared/ ./shared/

# Copy backend directory
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Run the application with hot reload
CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
