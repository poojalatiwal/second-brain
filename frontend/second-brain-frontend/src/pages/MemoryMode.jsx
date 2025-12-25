import { useState } from "react";
import client from "../api/axiosClient";

export default function MemoryMode() {
  const [input, setInput] = useState("");
  const [msgs, setMsgs] = useState([]);

  const send = async () => {
    const res = await client.post("/memory/chat", { message: input });
    setMsgs([...msgs, { user: input, bot: res.data.response }]);
    setInput("");
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Memory Mode</h2>

        {msgs.map((m, i)=>(
          <div key={i}>
            <div className="chat-user">{m.user}</div>
            <div className="chat-bot">{m.bot}</div>
          </div>
        ))}

        <input value={input} onChange={(e)=>setInput(e.target.value)} />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}
