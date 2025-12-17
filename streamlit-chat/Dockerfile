FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Copy shared directory (needed by streamlit-chat)
COPY shared/ ./shared/

# Copy streamlit-chat directory
COPY streamlit-chat/ ./streamlit-chat/

# Install dependencies
RUN uv sync --frozen --no-dev

# Expose port
EXPOSE 8501

# Run the application with hot reload
# baseUrlPath is required so Streamlit generates correct URLs when behind /chats/ proxy
CMD ["uv", "run", "streamlit", "run", "streamlit-chat/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
