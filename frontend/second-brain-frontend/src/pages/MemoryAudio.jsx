import { useState } from "react";
import { ingestAudio } from "../api/ingest";

export default function MemoryAudio() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadAudio = async () => {
    if (!file) {
      alert("Please select an audio file");
      return;
    }

    try {
      setLoading(true);
      await ingestAudio(file);
      alert("Audio added to memory");
      setFile(null);
    } catch (err) {
      console.error(err);
      alert("Failed to upload audio");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>🎧 Add Audio to Memory</h2>

      <input
        type="file"
        accept="audio/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      {file && (
        <p style={{ marginTop: "8px", color: "#94a3b8" }}>
          Selected: {file.name}
        </p>
      )}

      <button onClick={uploadAudio} disabled={loading}>
        {loading ? "Uploading..." : "Upload Audio"}
      </button>
    </div>
  );
}
