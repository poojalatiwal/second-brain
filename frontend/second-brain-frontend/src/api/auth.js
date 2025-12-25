import client from "./axiosClient";

export const signup = (data) => client.post("/auth/signup", data);
export const login = (data) => client.post("/auth/login", data);
