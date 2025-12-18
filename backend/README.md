# GoatBot Backend API

FastAPI backend application for GoatBot.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Auth0 environment variables:
```bash
export AUTH0_DOMAIN="your-tenant.auth0.com"
export AUTH0_CLIENT_ID="your-client-id"
export AUTH0_CLIENT_SECRET="your-client-secret"
export AUTH0_BASE_URL="goatbot.localhost"  # or your domain
export AUTH0_CALLBACK_URL="http://goatbot.localhost/api/auth/callback"  # optional, auto-generated if not set
```

3. Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Auth0 Setup

1. Create an Auth0 account at https://auth0.com
2. Create a new Application (Regular Web Application)
3. Configure allowed callback URLs: `http://goatbot.localhost/api/auth/callback`
4. Configure allowed logout URLs: `http://goatbot.localhost/`
5. Set the environment variables above with your Auth0 credentials

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
