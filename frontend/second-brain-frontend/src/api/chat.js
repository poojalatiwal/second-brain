import client from "./axiosClient";

export const sendChat = (text) =>
  client.post("/chat", { message: text });
