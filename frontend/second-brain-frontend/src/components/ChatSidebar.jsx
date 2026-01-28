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
      .then((res) => {
        const data = res.data;

        if (Array.isArray(data)) {
          setSessions(data);
        } else if (Array.isArray(data.sessions)) {
          setSessions(data.sessions);
        } else {
          setSessions([]);
        }
      })
      .catch(console.error);
  }, [refreshKey]);

  return (
    <div className="chat-sidebar">
      <button onClick={onNewChat}>+ New Chat</button>

      <div className="chat-history">
        {Array.isArray(sessions) &&
          sessions.map((s) => (
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
