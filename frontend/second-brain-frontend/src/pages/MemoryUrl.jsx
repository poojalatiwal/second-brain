import { useState } from "react";
import { ingestUrl } from "../api/ingest";
import "./MemoryHome.css";

export default function MemoryUrl() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const uploadUrl = async () => {
    if (!url.trim()) {
      alert("Enter a valid URL");
      return;
    }

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

      {/* URL input styled like file-input */}
      <input
        type="url"
        placeholder="https://example.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="file-input"
      />

      {/* Upload button */}
      <button
        className="upload-btn"
        onClick={uploadUrl}
        disabled={loading}
      >
        {loading ? "Adding..." : "Add Website"}
      </button>
    </div>
  );
}
