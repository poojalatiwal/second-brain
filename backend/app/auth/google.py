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
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# Google
@router.get("/google")
async def google_login(request: Request):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)

#  Google callback
@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    if not user_info:
        raise Exception("Failed to fetch user info from Google")

    email = user_info["email"]
    name = user_info.get("name", "")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            username=name,
            password_hash=None,  
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(user.id)

    return RedirectResponse(
        url=f"http://localhost:5173/oauth-success?token={access_token}"
    )
