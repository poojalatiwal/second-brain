import axios from "axios";

const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: false,
});

// ================= REQUEST =================
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

// ================= RESPONSE =================
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!error.response) {
      alert("Server unreachable");
      return Promise.reject(error);
    }

    if (error.response.status === 401) {
      localStorage.removeItem("token");
      if (!window.location.pathname.includes("/login")) {
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);


export const imageChat = (file) => {
  const form = new FormData();
  form.append("file", file);
  return axios.post("/chat/image", form);
};

export const pdfChat = (file) => {
  const form = new FormData();
  form.append("file", file);
  return axios.post("/chat/pdf", form);
};

export default axiosClient;
