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

  return axiosClient.post("/ingest/pdf", formData);
};

/* ================= IMAGE ================= */
export const ingestImage = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return axiosClient.post("/ingest/image", formData);
};

/* ================= AUDIO ================= */
export const ingestAudio = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return axiosClient.post("/ingest/audio", formData);
};

/* ================= URL ================= */
export const ingestUrl = (url) =>
  axiosClient.post("/ingest/url", null, {
    params: { url },
  });