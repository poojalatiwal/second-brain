import { useState } from "react";
import { ingestPdf } from "../api/ingest";

export default function MemoryPdf() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadPdf = async () => {
    if (!file) return alert("Select a PDF file");
    try {
      setLoading(true);
      await ingestPdf(file);
      alert("PDF added to memory");
      setFile(null);
    } catch {
      alert("Failed to upload PDF");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>📄 Add PDF to Memory</h2>

            <input
        type="file"
        className="file-input"
        accept="application/pdf"
        />

      <button onClick={uploadPdf} disabled={loading}>
        {loading ? "Uploading..." : "Upload PDF"}
      </button>
    </div>
  );
}
