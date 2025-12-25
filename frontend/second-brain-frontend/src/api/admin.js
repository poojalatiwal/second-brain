import client from "./axiosClient";

export const getUsers = () => client.get("/admin/users");
export const getLogs = () => client.get("/admin/logs");
export const getStats = () => client.get("/admin/stats");
