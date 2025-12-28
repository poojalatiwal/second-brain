import axiosClient from "./axiosClient";

/* ================= MEMORY CHAT ================= */
export const memoryChat = (question) =>
  axiosClient.post("/brain/", null, {
    params: { question },
  });

/* ================= HISTORY ================= */
export const getMemoryHistory = () =>
  axiosClient.get("/memory/history");

/* ================= DELETE MEMORY ================= */
export const deleteMemory = (id) =>
  axiosClient.delete(`/memory/delete/${id}`);

/* ================= UPDATE MEMORY ✅ REQUIRED ================= */
export const updateMemory = (id, newText) =>
  axiosClient.put(`/memory/update/${id}`, {
    new_text: newText,
  });
