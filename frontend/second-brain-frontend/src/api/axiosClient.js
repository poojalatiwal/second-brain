import axios from "axios";

const axiosClient = axios.create({
  baseURL: "http://localhost:8000", // change if needed
});

// 🔐 Attach JWT automatically
axiosClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default axiosClient;
