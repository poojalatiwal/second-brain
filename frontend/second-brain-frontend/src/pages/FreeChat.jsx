import { useEffect, useRef, useState } from "react";
import Navbar from "../components/Navbar";
import ChatSidebar from "../components/ChatSidebar";
import ChatInput from "../components/ChatInput";
import ChatBubble from "../components/ChatBubble";
import { streamChat, getChatHistory } from "../api/chat";
import "./FreeChat.css";

export default function FreeChat() {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [isStreaming, setIsStreaming] = useState(false);

  const chatBoxRef = useRef(null);

  /* ===== AUTO SCROLL ===== */
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop =
        chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  /* ===== LOAD CHAT HISTORY ===== */
  useEffect(() => {
    if (!sessionId) return;

    getChatHistory(sessionId)
      .then((res) => {
        setMessages(
          res.data.map((m) => ({
            role: m.role,
            text: m.content,
          }))
        );
      })
      .catch(console.error);
  }, [sessionId]);

  /* ===== SEND MESSAGE ===== */
  const sendMessage = async (text) => {
    if (!text.trim() || isStreaming) return;

    setIsStreaming(true);

    setMessages((prev) => [
      ...prev,
      { role: "user", text },
      { role: "ai", text: "" },
    ]);

    try {
      await streamChat({
        prompt: text,
        session_id: sessionId,

        onSession: (id) => {
          if (!sessionId) {
            setSessionId(id);
            setRefreshKey((k) => k + 1);
          }
        },

        onToken: ({ full }) => {
          setMessages((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = {
              role: "ai",
              text: full,
            };
            return updated;
          });
        },
      });
    } catch (err) {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "ai",
          text: "❌ Something went wrong. Please try again.",
        };
        return updated;
      });
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="chat-layout">
        <ChatSidebar
          sessionId={sessionId}
          refreshKey={refreshKey}
          onSelectSession={setSessionId}
          onNewChat={() => {
            setSessionId(null);
            setMessages([]);
          }}
        />

        <div className="chat-main">
          {/* ===== CHAT AREA ===== */}
          <div className="chat-box" ref={chatBoxRef}>
            {messages.length === 0 && (
              <div className="empty-chat">
                <h2>Start a new conversation</h2>
                <p>Ask anything to begin 🚀</p>
              </div>
            )}

            {messages.map((m, i) => (
              <ChatBubble
                key={i}
                role={m.role}
                text={m.text}
              />
            ))}
          </div>

              {/* ===== INPUT (ALWAYS VISIBLE) ===== */}
            <ChatInput
      onSend={sendMessage}
      disabled={isStreaming}
      sessionId={sessionId}
    />

        </div>
      </div>
    </>
  );
}
