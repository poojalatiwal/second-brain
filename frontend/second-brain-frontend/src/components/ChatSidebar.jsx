import { useEffect, useState } from "react";
import { getChatSessions } from "../api/chat";

export default function ChatSidebar({
  sessionId,
  refreshKey,
  onSelectSession,
  onNewChat,
}) {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    getChatSessions()
      .then((res) => setSessions(res.data))
      .catch(console.error);
  }, [refreshKey]); // 🔥 RELOAD WHEN refreshKey CHANGES

  return (
    <div className="chat-sidebar">
      <button onClick={onNewChat}>+ New Chat</button>

      <div className="chat-history">
        {sessions.map((s) => (
          <div
  key={s.id}
  className={`chat-item ${s.id === sessionId ? "active" : ""}`}
  onClick={() => onSelectSession(s.id)}
>
  {s.title}
</div>
        ))}
      </div>
    </div>
  );
}
