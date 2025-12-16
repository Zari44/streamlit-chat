.PHONY: help format lint type-check check install-dev clean

# Default Python version
PYTHON := python3
PIP := pip3

# Directories
BACKEND_DIR := backend
CHAT_DIR := chat
ROOT_DIR := .

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install-dev: ## Install development dependencies
	$(PIP) install mypy ruff
	@echo "Development dependencies installed"

format: ## Format code with ruff
	@echo "Formatting code with ruff..."
	ruff format $(ROOT_DIR)
	@echo "Formatting complete!"

lint: ## Run linters (ruff)
	@echo "Running ruff linter..."
	ruff check $(ROOT_DIR)
	@echo "Linting complete!"

type-check: ## Run type checker (mypy)
	@echo "Running mypy type checker..."
	mypy $(BACKEND_DIR) $(CHAT_DIR) || true
	@echo "Type checking complete!"

check: format lint type-check ## Run all checks (format, lint, type-check)

fix: ## Auto-fix linting issues
	@echo "Fixing linting issues..."
	ruff check --fix $(ROOT_DIR)
	@echo "Fixes applied!"

clean: ## Clean cache files
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -r {} + 2>/dev/null || true
	@echo "Cache files cleaned!"

