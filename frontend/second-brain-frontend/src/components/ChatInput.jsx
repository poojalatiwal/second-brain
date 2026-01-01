import { useState, useRef } from "react";
import VoiceRecorder from "./VoiceRecorder";
import { pdfChat, imageChat } from "../api/chat";

export default function ChatInput({ onSend, disabled = false, sessionId }) {
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

  // 👇 SHOW CONFIRMATION IN CHAT
  onSend(`📎 File attached: ${f.name}`);

  e.target.value = "";
};
  const submit = async () => {
    if (disabled) return;

    try {
      /* ===== FILE MODE ===== */
      if (file) {
        if (!text.trim()) {
          onSend("❗ Please ask a question about the file");
          return;
        }

        // show user messages
        onSend(`📎 ${file.name}`);
        onSend(text);

        let res;
        if (file.type.startsWith("image/")) {
          res = await imageChat(file, text, sessionId);
        } else if (file.type === "application/pdf") {
          res = await pdfChat(file, text, sessionId);
        } else {
          onSend("❌ Unsupported file type");
          return;
        }

        // AI answer
        onSend(res.data.answer);

        setFile(null);
        setText("");
        return;
      }

      /* ===== NORMAL CHAT ===== */
      if (text.trim()) {
        onSend(text);
        setText("");
      }
    } catch (err) {
      console.error(err);
      onSend("❌ Failed to process file");
    }
  };

  return (
    <div className="chat-input-bar">
      <button
        className="icon-btn"
        onClick={openFilePicker}
        title="Upload PDF or Image"
      >
        ➕
      </button>

        <input
    ref={fileRef}
    type="file"
    accept="application/pdf,image/*"
    style={{ display: "none" }}   // ✅ IMPORTANT
    onChange={handleFile}
  />

      <VoiceRecorder onResult={onSend} />

      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={
          file ? "Ask something about the file..." : "Ask anything..."
        }
        disabled={disabled}
        onKeyDown={(e) => e.key === "Enter" && submit()}
      />

      <button onClick={submit} disabled={disabled}>
        Send
      </button>
    </div>
  );
}
