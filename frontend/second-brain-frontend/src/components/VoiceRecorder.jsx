import { useState, useRef } from "react";
import { voiceChat } from "../api/chat";

export default function VoiceRecorder({ onResult }) {
  const [recording, setRecording] = useState(false);
  const mediaRecorder = useRef(null);
  const chunks = useRef([]);

  const start = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder.current = new MediaRecorder(stream);
    chunks.current = [];

    mediaRecorder.current.ondataavailable = (e) => {
      chunks.current.push(e.data);
    };

    mediaRecorder.current.onstop = async () => {
      const blob = new Blob(chunks.current, { type: "audio/webm" });
      const res = await voiceChat(blob);
      onResult(res.data.answer);
    };

    mediaRecorder.current.start();
    setRecording(true);
  };

  const stop = () => {
    mediaRecorder.current.stop();
    setRecording(false);
  };

  return (
    <button onClick={recording ? stop : start}>
      {recording ? "⏹ Stop" : "🎤"}
    </button>
  );
}
