import { ingestText } from "../api/ingest";
import { useState } from "react";

export default function Ingest() {
  const [text, setText] = useState("");

  return (
    <>
      <h2>Ingest</h2>
      <textarea onChange={e=>setText(e.target.value)} />
      <button onClick={()=>ingestText(text)}>Ingest Text</button>
    </>
  );
}
