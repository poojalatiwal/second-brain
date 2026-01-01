export default function ChatBubble({ role, text }) {
  return (
    <div className={`chat-row ${role}`}>
      <div className="chat-bubble">
        <div className="chat-role">
          {role === "user" ? "You" : "AI"}
        </div>
        <div className="chat-text">{text}</div>
      </div>
    </div>
  );
}
