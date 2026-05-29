import axios from "axios";

/**
 * Axios 인스턴스.
 * 베이스 URL은 .env 의 VITE_API_BASE_URL 사용.
 */
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  timeout: 10000,
});

export default apiClient;
