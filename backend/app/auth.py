"""Auth0 authentication utilities"""

import os
from functools import wraps
from typing import Annotated

import httpx
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from jose.constants import ALGORITHMS

# Load environment variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")
AUTH0_BASE_URL = os.getenv("AUTH0_BASE_URL", "")

# Auth0 configuration
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/" if AUTH0_DOMAIN else ""
AUTH0_AUTHORIZATION_URL = f"https://{AUTH0_DOMAIN}/authorize" if AUTH0_DOMAIN else ""
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token" if AUTH0_DOMAIN else ""
AUTH0_USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo" if AUTH0_DOMAIN else ""
AUTH0_LOGOUT_URL = f"https://{AUTH0_DOMAIN}/v2/logout" if AUTH0_DOMAIN else ""

# Security scheme
security = HTTPBearer(auto_error=False)


async def get_token_payload(token: str) -> dict:
    """Verify and decode JWT token from Auth0"""
    if not AUTH0_DOMAIN:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth0 not configured. Please set AUTH0_DOMAIN environment variable.",
        )

    # Get JWKS from Auth0
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    try:
        async with httpx.AsyncClient() as client:
            jwks_response = await client.get(jwks_url)
            jwks_response.raise_for_status()
            jwks = jwks_response.json()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch Auth0 JWKS: {str(e)}",
        )

    # Get the signing key
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
            break

    if not rsa_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to find appropriate key",
        )

    try:
        # Verify and decode the token
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=[ALGORITHMS.RS256],
            audience=AUTH0_AUDIENCE if AUTH0_AUDIENCE else None,
            issuer=AUTH0_ISSUER,
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
        )


async def get_current_user(
    request: Request,
    credentials: Annotated[HTTPBearer, Depends(security)] | None = None,
) -> dict:
    """Get current authenticated user from token (raises exception if not authenticated)"""
    # Try to get token from Authorization header
    token = None
    if credentials:
        token = credentials.credentials  # type: ignore[unresolved-attribute]
    else:
        # Try to get token from session cookie
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = await get_token_payload(token)
    return payload


async def get_current_user_optional(
    request: Request,
    credentials: Annotated[HTTPBearer, Depends(security)] | None = None,
) -> dict | None:
    """Get current authenticated user from token (returns None if not authenticated)"""
    # Try to get token from Authorization header
    token = None
    if credentials:
        token = credentials.credentials  # type: ignore[unresolved-attribute]
    else:
        # Try to get token from session cookie
        token = request.cookies.get("access_token")

    if not token:
        return None

    try:
        payload = await get_token_payload(token)
        return payload
    except HTTPException:
        return None


def require_auth(func):
    """Decorator to require authentication for a route"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        # This will be handled by the Depends() in the route
        return await func(*args, **kwargs)

    return wrapper
