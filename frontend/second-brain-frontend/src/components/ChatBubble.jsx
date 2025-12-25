export default function ChatBubble({ sender, text }) {
  return (
    <div className={sender === "user" ? "chat-user" : "chat-bot"}>
      {text}
    </div>
  );
}
