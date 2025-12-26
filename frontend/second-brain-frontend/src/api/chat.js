import axiosClient from "./axiosClient";

/* ================= MEMORY CHAT ================= */

// Ask from memory
export const memoryChat = (question) =>
  axiosClient.post("/memory/search", {
    query: question,
  });

// ✅ ADD THIS FUNCTION
export const getMemoryHistory = () =>
  axiosClient.get("/memory/history");
