import axios from "./axiosClient";

/* Get memory history */
export const getMemoryHistory = () =>
  axios.get("/memory/history");

// api/memory.js
export const memoryChat = (question) =>
  axios.post("/brain/memory", { question });

/* Delete memory */
export const deleteMemory = (id) =>
  axios.delete(`/memory/${id}`);

/* Update memory */
export const updateMemory = (id, text) =>
  axios.put(`/memory/${id}`, { text });
