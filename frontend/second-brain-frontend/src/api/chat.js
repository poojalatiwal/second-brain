import axios from "./axiosClient";

export const streamChat = async ({
  prompt,
  session_id,
  onToken,
  onDone,
  onSession,
}) => {
  const res = await fetch("http://localhost:8000/chat/stream", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify({ prompt, session_id }),
  });

  const sid = res.headers.get("X-Session-Id");
  if (sid) onSession?.(Number(sid));

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop();

    for (const event of events) {
      if (!event.startsWith("data: ")) continue;
      const payload = event.replace("data: ", "");

      if (payload === "[DONE]") {
        onDone?.();
        return;
      }

      onToken(JSON.parse(payload));
    }
  }
};

export const getChatSessions = () => axios.get("/chat/sessions");
export const getChatHistory = (id) => axios.get(`/chat/history/${id}`);


/* ================= VOICE CHAT ================= */
export const voiceChat = (audioFile) => {
  const fd = new FormData();
  fd.append("file", audioFile);
  return axios.post("/chat/audio", fd);
};

export const imageChat = (file, question, session_id) => {
  const fd = new FormData();
  fd.append("file", file);
  if (question) fd.append("question", question);
  if (session_id) fd.append("session_id", session_id);

  return axios.post("/chat/image", fd, {
    headers: { "Content-Type": "multipart/form-data" }
  });
};

export const pdfChat = (file, question, session_id) => {
  const fd = new FormData();
  fd.append("file", file);
  if (question) fd.append("question", question);
  if (session_id) fd.append("session_id", session_id);

  return axios.post("/chat/pdf", fd, {
    headers: { "Content-Type": "multipart/form-data" }
  });
};
