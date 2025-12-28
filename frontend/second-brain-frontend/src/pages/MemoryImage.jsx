import { useState } from "react";
import { ingestImage } from "../api/ingest";
import "./MemoryHome.css";

export default function MemoryImage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadImage = async () => {
    if (!file) {
      alert("Select an image");
      return;
    }

    try {
      setLoading(true);
      await ingestImage(file);
      alert("Image added to memory");
      setFile(null);
    } catch {
      alert("Failed to upload image");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>🖼️ Add Image to Memory</h2>

      {/* Upload section (same as PDF) */}
      <input
        type="file"
        accept="image/*"
        className="file-input"
        onChange={(e) => setFile(e.target.files[0])}
      />

      {/* Upload button */}
      <button
        className="upload-btn"
        onClick={uploadImage}
        disabled={loading}
      >
        {loading ? "Uploading..." : "Upload Image"}
      </button>
    </div>
  );
}
