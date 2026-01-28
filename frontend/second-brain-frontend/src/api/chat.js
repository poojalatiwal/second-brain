import axiosClient from "./axiosClient";

/* ================= STREAM CHAT ================= */

export const streamChat = async ({
  prompt,
  session_id,
  onToken,
  onDone,
  onSession,
}) => {
  const res = await fetch(
    `${import.meta.env.VITE_API_URL}/chat/stream`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ prompt, session_id }),
    }
  );

  if (!res.ok) {
    throw new Error("Stream request failed");
  }

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

/* ================= CHAT HISTORY ================= */

export const getChatSessions = () =>
  axiosClient.get("/chat/sessions");

export const getChatHistory = (id) =>
  axiosClient.get(`/chat/history/${id}`);


/* ================= VOICE CHAT ================= */

export const voiceChat = (audioFile) => {
  const fd = new FormData();
  fd.append("file", audioFile);
  return axiosClient.post("/chat/audio", fd);
};


/* ================= IMAGE CHAT ================= */

export const imageChat = (file, question, session_id) => {
  const fd = new FormData();
  fd.append("file", file);
  if (question) fd.append("question", question);
  if (session_id) fd.append("session_id", session_id);

  return axiosClient.post("/chat/image", fd);
};


/* ================= PDF CHAT ================= */

export const pdfChat = (file, question, session_id) => {
  const fd = new FormData();
  fd.append("file", file);
  if (question) fd.append("question", question);
  if (session_id) fd.append("session_id", session_id);

  return axiosClient.post("/chat/pdf", fd);
};