from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from groq import Groq

from app.config import settings
from app.auth.utils import get_current_user
from app.auth.models import User

router = APIRouter()
client = Groq(api_key=settings.GROQ_API_KEY)


@router.post("/")
async def stream_answer(
    prompt: str,
    current_user: dict = Depends(get_current_user)  # ✅ AUTH
):
    if not prompt.strip():
        raise HTTPException(400, "Prompt cannot be empty")

    def generate():
        # (Optional) first chunk can include metadata
        yield f"[user_id:{current_user["id"] }]\n"

        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.get("content"):
                yield chunk.choices[0].delta["content"]

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )
