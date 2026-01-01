import { Outlet, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";

import {
  memoryChat,
  getMemoryHistory,
  deleteMemory,
  updateMemory,
} from "../api/memory";


import { hybridSearch } from "../api/search";
import "./MemoryHome.css";


export default function MemoryHome() {
  const navigate = useNavigate();

  /* ================= ASK / EDIT ================= */
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loadingAsk, setLoadingAsk] = useState(false);
  const [editingMemory, setEditingMemory] = useState(null);

  /* ================= SEARCH ================= */
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResult, setSearchResult] = useState(null);
  const [loadingSearch, setLoadingSearch] = useState(false);

  /* ================= HISTORY ================= */
  const [history, setHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [selectedMemory, setSelectedMemory] = useState(null);
  const [openMenuId, setOpenMenuId] = useState(null);

  /* ================= LOAD HISTORY ================= */
  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoadingHistory(true);
      const res = await getMemoryHistory();
      setHistory(res.data.items || []);
    } catch {
      console.error("Failed to load history");
    } finally {
      setLoadingHistory(false);
    }
  };

  /* ================= SIDEBAR ACTIONS ================= */
  const newChat = () => {
    setQuestion("");
    setAnswer("");
    setSelectedMemory(null);
    setEditingMemory(null);
    setOpenMenuId(null);
  };

  const toggleMenu = (id) => {
    setOpenMenuId((prev) => (prev === id ? null : id));
  };

  const handleOpen = (item) => {
    setSelectedMemory(item);
    setEditingMemory(null);
    setQuestion("");
    setAnswer("");
    setOpenMenuId(null);
  };

  const handleEdit = (item) => {
    setEditingMemory(item);
    setQuestion(item.text);
    setSelectedMemory(null);
    setOpenMenuId(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this memory?")) return;

    try {
      await deleteMemory(id);
      setHistory((prev) => prev.filter((m) => m.id !== id));
      if (selectedMemory?.id === id) setSelectedMemory(null);
    } catch {
      alert("Failed to delete memory");
    }
  };

  /* ================= ASK / UPDATE ================= */
const askOrUpdate = async () => {
  if (!question.trim()) return;

  // EDIT MEMORY (unchanged)
  if (editingMemory) {
    try {
      setLoadingAsk(true);
      await updateMemory(editingMemory.id, question);
      setEditingMemory(null);
      await loadHistory();
      alert("Memory updated");
    } finally {
      setLoadingAsk(false);
    }
    return;
  }

  // 🧠 ASK FROM MEMORY
  try {
    setLoadingAsk(true);
    setAnswer("");

    const res = await memoryChat(question); // ✅ FIX

    setAnswer(res.data.answer);
  } catch (err) {
    console.error(err);
    setAnswer("Something went wrong");
  } finally {
    setLoadingAsk(false);
  }
};

  /* ================= SEARCH ================= */
  const searchMemory = async () => {
    if (!searchQuery.trim()) return;

    try {
      setLoadingSearch(true);
      const res = await hybridSearch(searchQuery);
      setSearchResult(res.data);
    } catch {
      setSearchResult(null);
    } finally {
      setLoadingSearch(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="memory-layout">
        {/* ========== LEFT SIDEBAR ========== */}
        <aside className="memory-sidebar">
           <button className="new-chat-btn" onClick={newChat}>
              ＋ New Chat
            </button>
          <div className="sidebar-header">
            <h3>📜 Memory History</h3>
          </div>

          {loadingHistory && <p className="muted">Loading...</p>}

          <div className="history-scroll">
            {history.map((item) => (
              <div
                key={item.id}
                className={`history-item ${
                  selectedMemory?.id === item.id ? "active" : ""
                }`}
                onClick={() => handleOpen(item)}
              >
               <div className="history-header">
  <span className="history-type">
    {item.modality?.toUpperCase()}
  </span>

  <button
    className="menu-btn"
    onClick={(e) => {
      e.stopPropagation();
      toggleMenu(item.id);
    }}
  >
    ⋮
  </button>

  {openMenuId === item.id && (
    <div className="menu-dropdown">
      <button onClick={() => handleOpen(item)}>Open</button>
      <button disabled>📌 Pin (soon)</button>
      <button
        className="danger"
        onClick={() => handleDelete(item.id)}
      >
        Delete
      </button>
    </div>
  )}
</div>


                <p className="history-preview">{item.preview}</p>
              </div>
            ))}
          </div>
        </aside>

        {/* ========== RIGHT PANEL ========== */}
        <main className="memory-main">
          {/* ===== MEMORY VIEW ===== */}
          {selectedMemory && (
            <div className="panel memory-viewer">
              <h3>📄 Memory</h3>
              <div className="memory-meta">
                <span>{selectedMemory.modality?.toUpperCase()}</span>
                {selectedMemory.source && <span>{selectedMemory.source}</span>}
              </div>
              <div className="memory-content">{selectedMemory.text}</div>
            </div>
          )}

          {/* ===== ASK / EDIT ===== */}
          <div className="panel">
            <h2>
              {editingMemory ? "✏️ Edit Memory" : "🧠 Ask from Memory"}
            </h2>

            <textarea
              placeholder={
                editingMemory
                  ? "Edit your memory text..."
                  : "Ask something from your stored memory..."
              }
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />

            <button className="upload-btn" onClick={askOrUpdate} disabled={loadingAsk}>
              {loadingAsk
                ? "Processing..."
                : editingMemory
                ? "Update Memory"
                : "Ask"}
            </button>

            {answer && (
              <div className="chat-answer">
                <strong>Answer:</strong>
                <p>{answer}</p>
              </div>
            )}
          </div>

          {/* ===== SEARCH ===== */}
         <div className="panel">
  <h2>🔍 Search Memory</h2>

  {/* Styled search input */}
  <input
    type="text"
    className="file-input"
    placeholder="Search keywords or concepts..."
    value={searchQuery}
    onChange={(e) => setSearchQuery(e.target.value)}
  />

  {/* Search button (same style as upload buttons) */}
  <button
    className="upload-btn"
    onClick={searchMemory}
    disabled={loadingSearch}
  >
    {loadingSearch ? "Searching..." : "Search"}
  </button>

  {/* Results */}
  {searchResult && (
    <div className="search-results">
      {searchResult.semantic.map((item, idx) => (
        <div key={idx} className="result-item">
          <p>{item.text}</p>
          <small>Score: {item.score.toFixed(3)}</small>
        </div>
      ))}
    </div>
  )}
</div>


          {/* ===== ADD ===== */}
          <h3 className="section-title">➕ Add to Memory</h3>

<div className="add-memory-grid">
  <div className="add-memory-card" onClick={() => navigate("text")}>
    <div className="icon">📝</div>
    <h4>Text</h4>
    <p>Add notes or paragraphs</p>
  </div>

  <div className="add-memory-card" onClick={() => navigate("pdf")}>
    <div className="icon">📄</div>
    <h4>PDF</h4>
    <p>Upload documents</p>
  </div>

  <div className="add-memory-card" onClick={() => navigate("image")}>
    <div className="icon">🖼️</div>
    <h4>Image</h4>
    <p>Extract text from images</p>
  </div>

  <div className="add-memory-card" onClick={() => navigate("url")}>
    <div className="icon">🌐</div>
    <h4>Website</h4>
    <p>Store webpage content</p>
  </div>

  <div className="add-memory-card" onClick={() => navigate("audio")}>
    <div className="icon">🎧</div>
    <h4>Audio</h4>
    <p>Speech & recordings</p>
  </div>
</div>

          <Outlet />
        </main>
      </div>
    </>
  );
}
