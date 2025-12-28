import { useState } from "react";
import { ingestPdf } from "../api/ingest";
import "./MemoryHome.css";
export default function MemoryPdf() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadPdf = async () => {
    if (!file) {
      alert("Select a PDF file");
      return;
    }

    try {
      setLoading(true);
      await ingestPdf(file);
      alert("PDF added to memory");
      setFile(null);
    } catch (err) {
      console.error(err);
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
        onChange={(e) => {
          const selectedFile = e.target.files[0];
          console.log("Selected PDF:", selectedFile); // ✅ DEBUG
          setFile(selectedFile); // ✅ THIS WAS MISSING
        }}
      />

      <button
  className="upload-btn"
  onClick={uploadPdf}
  disabled={loading}
>
  {loading ? "Uploading..." : "Upload PDF"}
</button>

    </div>
  );
}
