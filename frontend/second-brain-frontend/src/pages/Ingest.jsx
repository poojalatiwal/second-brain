import { useState } from "react";
import client from "../api/axiosClient";

export default function Ingest() {
  const [url, setUrl] = useState("");

  const send = async () => {
    await client.get("/ingest/url", { params: { url }});
    alert("Ingested!");
  };

  return (
    <div className="container">
      <div className="card">
        <h2>URL Ingest</h2>

        <input placeholder="Enter website URL" onChange={(e)=>setUrl(e.target.value)} />
        <button onClick={send}>Ingest</button>
      </div>
    </div>
  );
}
