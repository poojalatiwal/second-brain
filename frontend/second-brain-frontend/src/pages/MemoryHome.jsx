import { Outlet, useNavigate } from "react-router-dom";
import { useState } from "react";
import Navbar from "../components/Navbar";
import { memoryChat } from "../api/chat";
import "./MemoryHome.css";

export default function MemoryHome() {
  const navigate = useNavigate();
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askMemory = async () => {
    if (!question.trim()) return;
    try {
      setLoading(true);
      const res = await memoryChat(question);
      setAnswer(res?.data?.answer || "No answer found");
      setQuestion("");
    } catch {
      setAnswer("Error asking memory");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="memory-layout">
        {/* LEFT: HISTORY */}
        <aside className="memory-sidebar">
          <h3>📜 Memory History</h3>
          <p className="muted">No memory yet</p>
        </aside>

        {/* RIGHT */}
        <main className="memory-main">
          {/* 🔒 ASK FROM MEMORY (ALWAYS VISIBLE) */}
          <div className="panel">
            <h2>🧠 Ask from Memory</h2>

            <textarea
              placeholder="Ask something from your stored memory..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />

            <button onClick={askMemory} disabled={loading}>
              {loading ? "Thinking..." : "Ask"}
            </button>

            {answer && (
              <div className="chat-answer">
                <strong>Answer:</strong>
                <p>{answer}</p>
              </div>
            )}
          </div>

          {/* ➕ ADD TO MEMORY (HOME-LIKE BOXES) */}
          <h3 className="section-title">➕ Add to Memory</h3>

          <div className="memory-boxes">
            <div className="memory-card" onClick={() => navigate("text")}>
              📝
              <h4>Text</h4>
              <p>Add notes or paragraphs</p>
            </div>

            <div className="memory-card" onClick={() => navigate("pdf")}>
              📄
              <h4>PDF</h4>
              <p>Upload documents</p>
            </div>

            <div className="memory-card" onClick={() => navigate("image")}>
              🖼️
              <h4>Image</h4>
              <p>Extract text from images</p>
            </div>

            <div className="memory-card" onClick={() => navigate("url")}>
              🌐
              <h4>Website</h4>
              <p>Store webpage content</p>
            </div>

            <div className="memory-card" onClick={() => navigate("audio")}>
              🎧
              <h4>Audio</h4>
              <p>Speech & recordings</p>
            </div>
          </div>

          {/* 👇 SELECTED INGEST PAGE */}
          <Outlet />
        </main>
      </div>
    </>
  );
}
