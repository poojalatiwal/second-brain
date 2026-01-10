**Second Brain**

Second Brain is a full-stack AI-powered memory and knowledge assistant.
It allows users to chat with AI, upload documents, images, and audio, store them as personal memory, and later search, recall, and reason over their own data.

It acts as your personal “second brain” to store and interact with knowledge using AI.

## Features
- AI Chat (Streaming) – Real-time chat with AI
- Memory System – Store and retrieve personal knowledge
- PDF Upload & Chat – Ask questions from uploaded PDFs
- Image Understanding – Upload images and ask questions
- Audio Ingestion – Upload audio files and process them
- Hybrid Search – Keyword + semantic search over memory
- Authentication – Secure login & signup (JWT-based)
- Chat Sessions – Persistent chat history
- Admin APIs – User & system stats
- Dockerized – Fully containerized frontend & backend

# Tech Stack 

Frontend
- React + Vite
- Axios
- Streaming Fetch API
- Tailwind / Custom CSS
- Nginx (production)

Backend
- FastAPI
- SQLAlchemy
- JWT Authentication
- Qdrant (vector database)
- PostgreSQL
- Groq / LLM APIs

Infrastructure
- Docker

# How to run locally

- Backend
cd backend
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload

- Frontend
cd frontend/second-brain-frontend
npm install
npm run dev

# Run with Docker
docker compose down -v
docker compose build --no-cache
docker compose up

Then open : http://localhost:3000

# How It Works
- Files and chats are converted into embeddings
- Stored in Qdrant vector database
- Queries use semantic + hybrid search
- AI model answers using your personal memory
- Chat sessions and users are stored in PostgreSQL

# UI 

### Login Page
![Login](screenshots/login.png)

### Home Page
![Home](screenshots/home.png)

### Chat Interface
![Chat](screenshots/chat.png)

### Memory System
![Memory](screenshots/memory.png)

### Admin System
![Admin](screenshots/admin.png)