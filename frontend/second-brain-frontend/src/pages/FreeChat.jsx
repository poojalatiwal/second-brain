import { useState } from "react";

export default function FreeChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", text: input },
      {
        role: "ai",
        text: "This is a free AI response. Ask anything!",
      },
    ]);
    setInput("");
  };

  return (
    <div className="auth-page">
      <div className="auth" style={{ width: "700px" }}>
        <h2>🤖 Free AI Chat</h2>

        <div style={{ minHeight: "260px", marginBottom: "16px" }}>
          {messages.length === 0 && (
            <p style={{ color: "#94a3b8" }}>
              General AI assistant. No memory restriction.
            </p>
          )}

          {messages.map((msg, i) => (
            <div
              key={i}
              style={{
                marginBottom: "10px",
                color: msg.role === "user" ? "#60a5fa" : "#e5e7eb",
              }}
            >
              <strong>{msg.role === "user" ? "You" : "AI"}:</strong>{" "}
              {msg.text}
            </div>
          ))}
        </div>

        <input
          placeholder="Ask anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />

        <button className="primary" onClick={sendMessage}>
          Ask AI
        </button>
      </div>
    </div>
  );
}
