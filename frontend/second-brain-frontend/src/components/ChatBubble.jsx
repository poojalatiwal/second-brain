export default function ChatBubble({ role, text }) {
  return (
    <div style={{
      textAlign: role === "user" ? "right" : "left",
      margin: "10px 0"
    }}>
      <b>{role}</b>: {text}
    </div>
  );
}
