import { useState } from "react";
import { ingestText } from "../api/ingest";

export default function MemoryText() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const addText = async () => {
    if (!text.trim()) return alert("Please enter text");
    try {
      setLoading(true);
      await ingestText(text);
      alert("Text added to memory");
      setText("");
    } catch {
      alert("Failed to add text");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>📝 Add Text to Memory</h2>

      <textarea
        placeholder="Paste text to remember..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={addText} disabled={loading}>
        {loading ? "Adding..." : "Add Text"}
      </button>
    </div>
  );
}
