import axiosClient from "./axiosClient";

// Hybrid (semantic + keyword) search
export const hybridSearch = (query) =>
  axiosClient.get("/search/hybrid-search/", {
    params: { query },
  });