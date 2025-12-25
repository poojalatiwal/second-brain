import { useState } from "react";
import { sendChat } from "../api/chat";

export default function Chatbot() {
  const [input, setInput] = useState("");
  const [msgs, setMsgs] = useState([]);

  const send = async () => {
    const res = await sendChat(input);
    setMsgs([...msgs, { user: input, bot: res.data.response }]);
    setInput("");
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Chatbot</h2>

        {msgs.map((m, i) => (
          <div key={i}>
            <div className="chat-user">{m.user}</div>
            <div className="chat-bot">{m.bot}</div>
          </div>
        ))}

        <input value={input} onChange={(e) => setInput(e.target.value)} />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}
