import API from "./axiosClient";

export const ingestURL = (url) => API.post(`/ingest/url`, { url });

export const ingestPDF = (formData) =>
  API.post("/ingest/pdf", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

export const ingestImage = (formData) =>
  API.post("/ingest/image", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
