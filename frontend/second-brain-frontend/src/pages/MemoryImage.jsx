import { useState } from "react";
import { ingestImage } from "../api/ingest";

export default function MemoryImage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadImage = async () => {
    if (!file) return alert("Select an image");
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

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadImage} disabled={loading}>
        {loading ? "Uploading..." : "Upload Image"}
      </button>
    </div>
  );
}
