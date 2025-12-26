import api from "./axiosClient";

export const getUsers = () => api.get("/admin/users");
export const getLogs = () => api.get("/admin/logs");
export const getStats = () => api.get("/admin/stats");
