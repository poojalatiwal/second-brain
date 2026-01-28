import axiosClient from "./axiosClient";


export const hybridSearch = (query) =>
  axiosClient.get("/search/hybrid-search/", {
    params: { query },
  });