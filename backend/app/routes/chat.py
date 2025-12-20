# app/routes/chat.py
from openai import OpenAI

from fastapi import APIRouter, UploadFile, File
from groq import Groq
from app.config import settings
from pydantic import BaseModel
import requests
import base64

router = APIRouter()

groq_client = Groq(api_key=settings.GROQ_API_KEY)
client_vision = OpenAI(api_key=settings.OPENAI_API_KEY)

# ============================================================
# MODE 1 — TEXT CHAT (Groq)
# ============================================================
@router.post("/")
async def chat_text(prompt: str):
    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"answer": resp.choices[0].message.content}


# ============================================================
# MODE 2 — AUDIO CHAT (Groq Whisper)
# ============================================================
@router.post("/audio")
async def chat_audio(file: UploadFile = File(...)):
    audio_bytes = await file.read()

    transcript = groq_client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=(file.filename, audio_bytes)
    )

    text = transcript.text.strip()

    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": text}]
    )

    return {
        "you_said": text,
        "answer": resp.choices[0].message.content
    }


# ============================================================
# MODE 3 — IMAGE CHAT (DeepInfra Vision)
# ============================================================
@router.post("/image")
async def chat_image(file: UploadFile = File(...)):
    img_bytes = await file.read()
    b64 = base64.b64encode(img_bytes).decode()

    try:
        response = client_vision.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Explain this image clearly."},
                        {"type": "input_image", "image": b64},
                    ],
                }
            ]
        )

        answer = response.choices[0].message["content"]

    except Exception as e:
        answer = f"Vision Error: {str(e)}"

    return {"answer": answer}


# ============================================================
# MODE 4 — WEB SEARCH (SerpAPI + Groq)
# ============================================================
class WebQuery(BaseModel):
    query: str


@router.post("/web")
async def chat_web(data: WebQuery):

    serp = f"https://serpapi.com/search?q={data.query}&api_key={settings.SERPAPI_KEY}"

    try:
        resp = requests.get(serp).json()
        results = resp.get("organic_results", [])
    except:
        results = []

    context = "\n".join([
        f"{r.get('title')}: {r.get('snippet')}"
        for r in results[:5]
    ])

    prompt = f"""
Use ONLY this information to answer the question:

{context}

Question: {data.query}
"""

    reply = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "results_used": results[:5],
        "answer": reply.choices[0].message.content
    }
