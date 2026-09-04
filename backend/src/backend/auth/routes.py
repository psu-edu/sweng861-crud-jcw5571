from fastapi import APIRouter, Request

from backend.auth.oauth import oauth


router = APIRouter()


@router.get("/auth/login")
async def login(request: Request):
    # Build Google's authorization URL and redirect the user's browser there.
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/callback", name="auth_callback")
async def auth_callback(request: Request):
    # Exchange Google's authorization code for tokens.
    token = await oauth.google.authorize_access_token(request)

    return {
        "message": "Google authentication successful",
        "token_type": token.get("token_type"),
    }
