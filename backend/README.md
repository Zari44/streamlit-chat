# GoatBot Backend API

FastAPI backend application for GoatBot.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── app/
│   ├── __init__.py
│   ├── routers/           # API route handlers
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── example.py
│   └── models/            # Pydantic models
│       ├── __init__.py
│       └── example.py
```

