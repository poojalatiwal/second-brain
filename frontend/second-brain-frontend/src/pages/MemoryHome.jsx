import { useEffect, useState } from "react";
import { memoryChat, getMemoryHistory } from "../api/chat";
import {
  ingestText,
  ingestPdf,
  ingestImage,
  ingestAudio,
  ingestUrl,
} from "../api/ingest";
import Navbar from "../components/Navbar";

export default function MemoryChat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [history, setHistory] = useState([]);

  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  /* ================= LOAD HISTORY ================= */
  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const res = await getMemoryHistory();
      setHistory(res?.data?.results || []);
    } catch (err) {
      console.warn("History not available yet");
      setHistory([]);
    }
  };

  /* ================= ASK MEMORY ================= */
  const askMemory = async () => {
    if (!question.trim()) return;

    try {
      setLoading(true);
      const res = await memoryChat(question);
      setAnswer(res?.data?.answer || "No answer found");
      setQuestion("");
      loadHistory();
    } catch (err) {
      setAnswer("Error querying memory");
    } finally {
      setLoading(false);
    }
  };

  /* ================= INGEST ================= */
  const handleIngestText = async () => {
    if (!text.trim()) return alert("Enter text first");
    await ingestText(text);
    setText("");
    alert("Text added to memory");
    loadHistory();
  };

  const handleIngestUrl = async () => {
    if (!url.trim()) return alert("Enter URL first");
    await ingestUrl(url);
    setUrl("");
    alert("URL added to memory");
    loadHistory();
  };

  const uploadFile = async (fn, file) => {
    if (!file) return;
    await fn(file);
    alert("File added to memory");
    loadHistory();
  };

  return (
    <>
      <Navbar />

      <div className="chat-layout">
        {/* ===== LEFT: HISTORY ===== */}
        <aside className="chat-history">
          <h3>📜 Memory History</h3>

          {history.length === 0 && (
            <p className="muted">No memory yet</p>
          )}

          {history.map((h, i) => (
            <div key={i} className="history-item">
              {h.question || h.text || "Memory item"}
            </div>
          ))}
        </aside>

        {/* ===== RIGHT: MAIN ===== */}
        <section className="chat-main">
          {/* ===== ASK MEMORY ===== */}
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

          {/* ===== ADD MEMORY ===== */}
          <div className="panel">
            <h2>➕ Add to Memory</h2>

            {/* TEXT */}
            <div className="ingest-row">
              <label>📝 Text</label>
              <textarea
                placeholder="Paste text to remember..."
                value={text}
                onChange={(e) => setText(e.target.value)}
              />
              <button onClick={handleIngestText}>Add Text</button>
            </div>

            {/* URL */}
            <div className="ingest-row">
              <label>🌐 Website URL</label>
              <input
                placeholder="https://example.com"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
              <button onClick={handleIngestUrl}>Add URL</button>
            </div>

            {/* FILES */}
            <div className="ingest-grid">
              <div>
                <label>📄 PDF</label>
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={(e) =>
                    uploadFile(ingestPdf, e.target.files[0])
                  }
                />
              </div>

              <div>
                <label>🖼️ Image</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) =>
                    uploadFile(ingestImage, e.target.files[0])
                  }
                />
              </div>

              <div>
                <label>🎧 Audio</label>
                <input
                  type="file"
                  accept="audio/*"
                  onChange={(e) =>
                    uploadFile(ingestAudio, e.target.files[0])
                  }
                />
              </div>
            </div>
          </div>
        </section>
      </div>
    </>
  );
}
