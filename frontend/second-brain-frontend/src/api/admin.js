import axiosClient from "./axiosClient";

export const getAdminUsers = () =>
  axiosClient.get("/admin/users");

export const getAdminLogs = () =>
  axiosClient.get("/admin/logs");

export const getAdminStats = () =>
  axiosClient.get("/admin/stats");
