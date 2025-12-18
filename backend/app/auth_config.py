"""Auth0 configuration"""

import os

from dotenv import load_dotenv

load_dotenv()

# Auth0 Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_BASE_URL = os.getenv("AUTH0_BASE_URL", os.getenv("DOMAIN_URL", "goatbot.localhost"))
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", f"http://{AUTH0_BASE_URL}/api/auth/callback")

# Auth0 URLs
AUTH0_AUTHORIZE_URL = f"https://{AUTH0_DOMAIN}/authorize"
AUTH0_ACCESS_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
AUTH0_USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"
AUTH0_LOGOUT_URL = f"https://{AUTH0_DOMAIN}/v2/logout"
