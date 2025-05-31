import axios from "axios";

const api = axios.create({
  baseURL: "http://92.255.78.34:8000/api/v1",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("jwt_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;