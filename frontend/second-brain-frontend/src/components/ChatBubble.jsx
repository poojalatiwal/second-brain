import ReactMarkdown from "react-markdown";
import "./ChatBubble.css";

export default function ChatBubble({ role, text }) {
  return (
    <div className={`chat-row ${role}`}>
      <div className="chat-bubble">
        <div className="chat-role">
          {role === "user" ? "You" : "AI"}
        </div>

        <div className="chat-text">
          <ReactMarkdown>{text}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
