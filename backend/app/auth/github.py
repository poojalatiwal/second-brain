from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
import os

from app.db.postgree import get_db
from app.auth.models import User
from app.auth.utils import create_access_token

router = APIRouter(prefix="/auth", tags=["OAuth"])

oauth = OAuth()

oauth.register(
    name="github",
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)

# STEP 1 → Redirect to GitHub
@router.get("/github")
async def github_login(request: Request):
    redirect_uri = os.getenv("GITHUB_REDIRECT_URI")
    return await oauth.github.authorize_redirect(request, redirect_uri)

# STEP 2 → GitHub callback
@router.get("/github/callback")
async def github_callback(
    request: Request,
    db: Session = Depends(get_db)
):
    token = await oauth.github.authorize_access_token(request)

    resp = await oauth.github.get("user", token=token)
    user_info = resp.json()

    email = user_info.get("email")

    # GitHub may not return email directly
    if not email:
        emails_resp = await oauth.github.get("user/emails", token=token)
        emails = emails_resp.json()
        email = next(e["email"] for e in emails if e["primary"])

    username = user_info.get("login")

    # find or create user
    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            username=username,
            password_hash=None,
            auth_provider="github",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(user.id)

    return RedirectResponse(
        url=f"http://localhost:5173/oauth-success?token={access_token}"
    )
