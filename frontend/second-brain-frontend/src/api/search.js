import axiosClient from "./axiosClient";

//hybrid search
export const hybridSearch = (query) =>
  axiosClient.get("/search/hybrid-search/", {
    params: { query },
  });