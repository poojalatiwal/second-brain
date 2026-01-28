
import { useNavigate } from "react-router-dom";
import "./Home.css";

export default function Home() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="home-container">
      <header className="topbar">
        <div className="brand">
          🧠 <span>SecondBrain AI</span>
        </div>

        <div className="top-actions">
          <button onClick={() => navigate("/")}>Home</button>
          <button className="logout-btn" onClick={logout}>
            Logout
          </button>
        </div>
      </header>

      <main className="home-main">
        <h1>Welcome to SecondBrain AI</h1>
        <p className="subtitle">
          Your personal AI assistant that remembers your knowledge.
        </p>

        <div className="mode-container">
          <div
            className="mode-card"
            onClick={() => navigate("/memory")}
          >
            <span className="mode-icon">📚</span>
            <h3>Memory Chat</h3>
            <p>Ask questions from your stored knowledge base</p>
          </div>

          <div
            className="mode-card"
            onClick={() => navigate("/free-chat")}
          >
            <span className="mode-icon">🤖</span>
            <h3>AI Chat</h3>
            <p>General AI assistant for free conversation</p>
          </div>
        </div>
      </main>
    </div>
  );
}
