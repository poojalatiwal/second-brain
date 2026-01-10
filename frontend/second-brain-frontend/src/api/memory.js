import axiosClient from "./axiosClient";

/* Get memory history */
export const getMemoryHistory = () =>
  axiosClient.get("/memory/history");

/* Ask from memory */
export const memoryChat = (question) =>
  axiosClient.post("/brain/memory/", { question }); 

/* Delete memory */
export const deleteMemory = (id) =>
  axiosClient.delete(`/memory/${id}`);

/* Update memory */
export const updateMemory = (id, text) =>
  axiosClient.put(`/memory/${id}`, { text });
