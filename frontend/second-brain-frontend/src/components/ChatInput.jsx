import { useState, useRef } from "react";
import VoiceRecorder from "./VoiceRecorder";

export default function ChatInput({ onSend, disabled = false }) {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const fileRef = useRef(null);

  const openFilePicker = () => {
    if (!disabled) fileRef.current.click();
  };

  const handleFile = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    setFile(f);
    e.target.value = "";
  };

  const removeFile = () => setFile(null);

  const submit = () => {
    if (disabled) return;

    if (!text.trim() && !file) return;

    onSend({ text, file });

    setText("");
    setFile(null);
  };

  return (
    <div className="chat-input-wrapper">
      {/* FILE PREVIEW */}
      {file && (
        <div className="file-preview">
          <span>📄 {file.name}</span>
          <button onClick={removeFile}>✕</button>
        </div>
      )}

      <div className="chat-input-bar">
       <button className="icon-btn" onClick={openFilePicker}>
  +
</button>

        <input
          ref={fileRef}
          type="file"
          accept="application/pdf,image/*"
          hidden
          onChange={handleFile}
        />

        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={
            file ? `Ask something about ${file.name}...` : "Ask anything..."
          }
          disabled={disabled}
          onKeyDown={(e) => e.key === "Enter" && submit()}
        />

        <VoiceRecorder onResult={(t) => setText(t)} />

        <button onClick={submit} disabled={disabled}>Send</button>
      </div>
    </div>
  );
}
