from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from groq import Groq
from app.config import settings

router = APIRouter()
client = Groq(api_key=settings.GROQ_API_KEY)

@router.post("/")
async def stream_answer(prompt: str):
    def generate():
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.get("content"):
                yield chunk.choices[0].delta["content"]

    return StreamingResponse(generate(), media_type="text/plain")
