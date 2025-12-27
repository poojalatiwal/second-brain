import { useState } from "react";
import { ingestUrl } from "../api/ingest";

export default function MemoryUrl() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const addUrl = async () => {
    if (!url.trim()) return alert("Enter a valid URL");
    try {
      setLoading(true);
      await ingestUrl(url);
      alert("Website added to memory");
      setUrl("");
    } catch {
      alert("Failed to add website");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>🌐 Add Website to Memory</h2>

      <input
        placeholder="https://example.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <button onClick={addUrl} disabled={loading}>
        {loading ? "Adding..." : "Add Website"}
      </button>
    </div>
  );
}
