from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from groq import Groq
import json, base64
from typing import List
from datetime import datetime
from io import BytesIO
from pypdf import PdfReader

from app.config import settings
from app.db.postgree import get_db
from app.auth.utils import get_current_user
from app.auth.models import ChatSession, ChatMessage, User

router = APIRouter(prefix="/chat", tags=["Chat"])
groq = Groq(api_key=settings.GROQ_API_KEY)

# ======================= MODELS =======================

class TextChat(BaseModel):
    prompt: str
    session_id: int | None = None


class ChatSessionOut(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        orm_mode = True


# ======================= HELPERS =======================

def make_title(text: str) -> str:
    text = text.strip()
    return text[:60] if len(text) > 5 else "Conversation"


# ======================= STREAMING =======================

def stream_llm(prompt: str, session: ChatSession, db: Session):
    full_answer = ""

    completion = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    for chunk in completion:
        token = chunk.choices[0].delta.content
        if token:
            full_answer += token
            yield f"data: {json.dumps({'token': token, 'full': full_answer})}\n\n"

    db.add(ChatMessage(
        session_id=session.id,
        role="ai",
        modality="text",
        content=full_answer
    ))
    db.commit()

    yield "data: [DONE]\n\n"


# ======================= TEXT CHAT =======================

@router.post("/stream")
def chat_stream(
    data: TextChat,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    session = None

    if data.session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == data.session_id,
            ChatSession.user_id == user.id
        ).first()

    if not session:
        session = ChatSession(
            user_id=user.id,
            title=make_title(data.prompt)
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # 🔥 AUTO CONTEXT INJECTION (KEY PART)
    prompt = data.prompt
    if session.active_context:
        prompt = f"""
You have access to the following context ({session.context_type}):

{session.active_context}

User question:
{data.prompt}
"""

    db.add(ChatMessage(
        session_id=session.id,
        role="user",
        modality="text",
        content=data.prompt
    ))
    db.commit()

    return StreamingResponse(
        stream_llm(prompt, session, db),
        media_type="text/event-stream",
        headers={"X-Session-Id": str(session.id)}
    )


# ======================= IMAGE CHAT =======================

@router.post("/image")
async def chat_image(
    file: UploadFile = File(...),
    question: str | None = None,
    session_id: int | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode()

    prompt = question or "Explain this image"

    session = None
    if session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user.id
        ).first()

    if not session:
        session = ChatSession(user_id=user.id, title=make_title(prompt))
        db.add(session)
        db.commit()
        db.refresh(session)

    res = groq.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }}
            ]
        }]
    )

    answer = res.choices[0].message.content

    # 🔥 STORE CONTEXT FOR FUTURE QUESTIONS
    session.active_context = answer
    session.context_type = "image"
    db.commit()

    db.add_all([
        ChatMessage(session_id=session.id, role="user", modality="image",
                    content=f"{prompt} ({file.filename})"),
        ChatMessage(session_id=session.id, role="ai", modality="image",
                    content=answer)
    ])
    db.commit()

    return {"answer": answer, "session_id": session.id}


# ======================= PDF CHAT =======================

@router.post("/pdf")
async def chat_pdf(
    file: UploadFile = File(...),
    question: str | None = None,
    session_id: int | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    reader = PdfReader(BytesIO(await file.read()))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    text = text[:12000]

    if not text.strip():
        return {"answer": "No readable text found in PDF"}

    session = None
    if session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user.id
        ).first()

    if not session:
        session = ChatSession(user_id=user.id, title=make_title(file.filename))
        db.add(session)
        db.commit()
        db.refresh(session)

    prompt = f"""
Document content:
{text}

User question:
{question or "Summarize the document"}
"""

    res = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = res.choices[0].message.content

    # 🔥 STORE CONTEXT
    session.active_context = text
    session.context_type = "pdf"
    db.commit()

    db.add_all([
        ChatMessage(session_id=session.id, role="user", modality="pdf",
                    content=question or f"Uploaded PDF: {file.filename}"),
        ChatMessage(session_id=session.id, role="ai", modality="pdf",
                    content=answer)
    ])
    db.commit()

    return {"answer": answer, "session_id": session.id}


# ======================= SESSION LIST =======================

@router.get("/sessions", response_model=List[ChatSessionOut])
def list_sessions(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user.id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )


@router.get("/history/{session_id}")
def get_history(
    session_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
        .all()
    )
