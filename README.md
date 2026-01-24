# 🧠 Second Brain – AI-Powered Knowledge Assistant

Second Brain is a **full-stack AI-powered memory and knowledge assistant**.  
It allows users to chat with AI, upload documents, images, audio, and URLs, store them as personal memory, and later **search, recall, and reason over their own data**.

It acts as your personal **“second brain”** to store and interact with knowledge using AI.

---

## 📌 Purpose of the Project

The purpose of this project is to build an intelligent system that helps users **store, organize, and interact with personal knowledge** using modern AI models and vector search.

The application is designed to be:
- Scalable
- Secure
- Fast
- Memory-efficient
- Developer-friendly

---

## 🛠️ Tech Stack

### Frontend
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-38BDF8?style=for-the-badge&logo=tailwind-css&logoColor=white)

### Backend
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CC2927?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

### Databases
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-FF4F00?style=for-the-badge&logo=qdrant&logoColor=white)

### AI & APIs
![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![SentenceTransformers](https://img.shields.io/badge/Sentence--Transformers-4B8BBE?style=for-the-badge)

### Infrastructure
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

---

## ✨ Features

- 🔹 AI Chat (Streaming) – Real-time chat with AI models
- 🔹 Memory System – Store and retrieve personal knowledge
- 🔹 PDF Upload & Chat – Ask questions from uploaded PDFs
- 🔹 Image Understanding – Upload images and ask questions
- 🔹 Audio Ingestion – Upload audio files and process them
- 🔹 URL Ingestion – Save and understand website content
- 🔹 Hybrid Search – Keyword + semantic search over memory
- 🔹 Authentication – Secure JWT-based login & signup
- 🔹 Chat Sessions – Persistent chat history
- 🔹 Admin APIs – User and system analytics
- 🔹 Fully Dockerized – Frontend + Backend + Databases

---

## 🏗️ Architecture

The **Second Brain** application follows a modular, service-oriented architecture:

- **Frontend (React + Vite)**  
  Handles UI, authentication, chat streaming, and file uploads.

- **Backend (FastAPI)**  
  Manages authentication, ingestion pipelines, embeddings, memory logic, and AI interaction.

- **Vector Database (Qdrant)**  
  Stores embeddings for semantic and hybrid search.

- **Relational Database (PostgreSQL)**  
  Stores users, chat sessions, messages

- **AI Layer**  
  Uses Groq / OpenAI APIs for reasoning and responses.

---

## ⚙️ How It Works

1. Files, chats, images, and URLs are converted into embeddings
2. Embeddings are stored in **Qdrant vector database**
3. User queries trigger **semantic + hybrid search**
4. Relevant memory is retrieved
5. AI model generates answers using personal context
6. Chats and users are stored in **PostgreSQL**

---

## ▶️ Run Locally

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload

### Backend
cd frontend/second-brain-frontend
npm install
npm run dev


## ▶️ Run with Docker

# Run with Docker
docker compose down -v
docker compose build --no-cache
docker compose up

Then open : http://localhost:3000

---

<hr style="border: 1px solid white; margin-top: 20px;">

<h1 style="color:#1E90FF;">UI Screenshots</h1>

<h3 style="color:#1E90FF;">Login Page</h3>
<img src="./screenshots/login.png" alt="Login" />

<h3 style="color:#1E90FF;">Home Page</h3>
<img src="./screenshots/home.png" alt="Home" />

<h3 style="color:#1E90FF;">Chat Interface</h3>
<img src="./screenshots/chat.png" alt="Chat" />

<h3 style="color:#1E90FF;">Memory System</h3>
<img src="./screenshots/memory.png" alt="Memory" />

<h3 style="color:#1E90FF;">Admin System</h3>
<img src="./screenshots/admin.png" alt="Admin" />
