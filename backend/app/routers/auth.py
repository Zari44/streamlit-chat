"""Auth0 authentication router"""

import secrets
import traceback
from urllib.parse import urlencode

import httpx
from authlib.integrations.httpx_client import AsyncOAuth2Client
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from jose import jwt

from backend.app.auth_config import (
    AUTH0_CALLBACK_URL,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_DOMAIN,
    AUTH0_USERINFO_URL,
)
from shared.logger import get_logger

router = APIRouter()


logger = get_logger(__name__)


def get_session_token(request: Request) -> str | None:
    """Get session token from cookie"""
    return request.cookies.get("session_token")


@router.get("/login")
async def login():
    """Initiate Auth0 login flow"""

    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Configuration is missing")
    # 1. Generate state for CSRF protection
    state = secrets.token_urlsafe(32)

    # 2. Build authorization URL
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "state": state,
    }

    # Ensure the domain doesn't have an accidental https:// prefix in the variable
    domain = AUTH0_DOMAIN.removeprefix("https://").removeprefix("http://")
    authorize_url = f"https://{domain}/authorize?{urlencode(params)}"

    # 3. Create the Redirect response
    response = RedirectResponse(url=authorize_url)

    # 4. Store state in cookie for validation in the /callback route
    response.set_cookie(
        key="auth_state",
        value=state,
        httponly=True,  # Prevents JavaScript access
        samesite="lax",  # Necessary for cross-site redirects
        secure=False,  # Set to True in production (HTTPS)
        max_age=600,  # 10 minutes
    )

    return response


@router.get("/callback")
async def callback(request: Request, code: str, state: str | None = None):
    """Handle Auth0 callback"""
    # Validate state
    stored_state = request.cookies.get("auth_state")
    if not stored_state or stored_state != state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state parameter",
        )

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code not provided",
        )

    # Exchange code for tokens
    async with AsyncOAuth2Client(
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
    ) as client:
        try:
            token_response = await client.fetch_token(
                url=f"https://{AUTH0_DOMAIN}/oauth/token",
                code=code,
                redirect_uri=AUTH0_CALLBACK_URL,
            )

            access_token = token_response.get("access_token")
            id_token = token_response.get("id_token")

            if not access_token or not id_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to obtain tokens",
                )

            # Get user info
            async with httpx.AsyncClient() as http_client:
                userinfo_response = await http_client.get(
                    AUTH0_USERINFO_URL,
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                userinfo_response.raise_for_status()
                userinfo_response.json()

            # Create response with redirect to home
            response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

            # Store tokens in cookies
            response.set_cookie(
                key="session_token",
                value=id_token,
                httponly=True,
                samesite="lax",
                secure=False,  # Set to True in production with HTTPS
                path="/",
                max_age=3600 * 24,  # 24 hours
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                samesite="lax",
                secure=False,  # Set to True in production with HTTPS
                path="/",
                max_age=3600 * 24,  # 24 hours
            )

            # Clear auth state cookie
            response.delete_cookie("auth_state")

            return response

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Authentication failed: {str(e)}",
            ) from e


@router.get("/logout")
async def logout(request: Request):
    """Logout user and clear session"""
    # Clear all session cookies and redirect to home
    # This performs local logout. For Auth0 logout, configure the returnTo URL
    # in Auth0 Dashboard -> Applications -> Allowed Logout URLs
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    # Clear all session cookies
    response.delete_cookie("session_token", path="/")
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("auth_state", path="/")

    return response


@router.get("/me")
async def get_current_user(request: Request):
    """Get current authenticated user info"""
    id_token = get_session_token(request)
    if not id_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        # Decode JWT token (no verification needed as it's from Auth0 callback)
        # In production, you should verify the token signature
        payload = jwt.decode(
            id_token,
            key=None,
            algorithms=["RS256"],
            options={
                "verify_signature": False,  # Skip signature verification for now
                "verify_aud": False,  # Skip audience validation
            },
        )
        return {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "name": payload.get("name"),
            "nickname": payload.get("nickname"),
            "picture": payload.get("picture"),
        }
    except jwt.JWTError as e:
        logger.error(f"Line 206: JWTError: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from e


def get_current_user_dependency(request: Request) -> dict:
    """Dependency to get current authenticated user"""
    id_token = get_session_token(request)
    if not id_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = jwt.decode(
            id_token,
            key=None,
            algorithms=["RS256"],
            options={
                "verify_signature": False,  # Skip signature verification for now
                "verify_aud": False,  # Skip audience validation
            },
        )
        return {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "name": payload.get("name"),
            "nickname": payload.get("nickname"),
            "picture": payload.get("picture"),
        }
    except jwt.JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from e
