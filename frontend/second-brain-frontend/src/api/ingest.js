import axiosClient from "./axiosClient";

/* ================= TEXT ================= */
export const ingestText = (text) =>
  axiosClient.post("/ingest/text", null, {
    params: { text },
  });

/* ================= PDF ================= */
export const ingestPdf = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return axiosClient.post("/ingest/pdf", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

/* ================= IMAGE ================= */
export const ingestImage = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return axiosClient.post("/ingest/image", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

/* ================= AUDIO ================= */
export const ingestAudio = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return axiosClient.post("/ingest/audio", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

/* ================= URL ================= */
export const ingestUrl = (url) =>
  axiosClient.post("/ingest/url", null, {
    params: { url },
  });
