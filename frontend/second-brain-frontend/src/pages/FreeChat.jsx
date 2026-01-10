import { useEffect, useRef, useState } from "react";
import Navbar from "../components/Navbar";
import ChatSidebar from "../components/ChatSidebar";
import ChatInput from "../components/ChatInput";
import ChatBubble from "../components/ChatBubble";
import { streamChat, getChatHistory, pdfChat, imageChat } from "../api/chat";
import "./FreeChat.css";

export default function FreeChat() {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const chatBoxRef = useRef(null);

  /* ================= AUTO SCROLL ================= */
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  /* ================= LOAD HISTORY ================= */
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

  /* ================= SEND MESSAGE ================= */
  const sendMessage = async ({ text, file }) => {
    if (isStreaming) return;
    setIsStreaming(true);

    // show user message (only if text exists)
    if (text?.trim()) {
      setMessages((prev) => [...prev, { role: "user", text }]);
    }

    try {
      /* ========== FILE MODE ========== */
      if (file instanceof File) {
        let res;

        if (file.type === "application/pdf") {
          res = await pdfChat(file, text, sessionId);
        } else if (file.type.startsWith("image/")) {
          res = await imageChat(file, text, sessionId);
        } else {
          throw new Error("Unsupported file");
        }

        // AI response
        setMessages((prev) => [
          ...prev,
          { role: "ai", text: res.data.answer },
        ]);

        // 🔒 create session ONCE
        if (!sessionId && res.data.session_id) {
          setSessionId(res.data.session_id);
        }

        return;
      }

      /* ========== TEXT CHAT (NORMAL) ========== */
      setMessages((prev) => [...prev, { role: "ai", text: "" }]);

      await streamChat({
        prompt: text,
        session_id: sessionId, // ✅ ALWAYS reuse session
        onSession: (id) => {
          if (!sessionId) setSessionId(id);
        },
        onToken: ({ full }) => {
          setMessages((prev) => {
            const copy = [...prev];
            copy[copy.length - 1] = { role: "ai", text: full };
            return copy;
          });
        },
      });

    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: "❌ Error processing request" },
      ]);
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
          onSelectSession={setSessionId}
          onNewChat={() => {
            setSessionId(null);
            setMessages([]);
          }}
        />

        <div className="chat-main">
                 <div className="chat-box" ref={chatBoxRef}>
  {messages.length === 0 ? (
    <div className="chat-empty">
      <h2>🤖 Hi, I’m your Second Brain</h2>
      <p>
        Start typing, upload a file, or ask me to recall something for you.
      </p>
    </div>
  ) : (
    messages.map((m, i) => (
      <ChatBubble key={i} role={m.role} text={m.text} />
    ))
  )}
</div>

          <ChatInput onSend={sendMessage} disabled={isStreaming} />
        </div>
      </div>
    </>
  );
}
