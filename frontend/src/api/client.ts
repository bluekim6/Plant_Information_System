import axios from "axios";

/**
 * Axios 인스턴스.
 *
 * 기본값은 빈 문자열(상대경로) 이다. 이렇게 하면 모든 /api/* 요청이
 * 프론트엔드와 동일 origin(예: 5173) 으로 나가고, Vite dev server proxy
 * (vite.config.ts) 가 이를 백엔드(8000) 로 전달한다.
 * 도면 PDF(buildDrawingUrl) 와 동일한 same-origin 방식이라,
 * cross-origin 요청을 차단하는 사내 보안정책을 우회할 수 있다.
 *
 * 별도 절대 URL 이 필요한 환경에서만 .env 의 VITE_API_BASE_URL 을 지정한다.
 */
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "",
  timeout: 10000,
});

export default apiClient;
