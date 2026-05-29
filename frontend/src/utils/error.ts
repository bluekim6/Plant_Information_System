import axios from "axios";
import type { ApiErrorBody } from "../types/common";

/** 백엔드의 통일 에러 응답에서 사용자에게 보여줄 메시지를 추출한다. */
export function extractErrorMessage(err: unknown): string {
  if (axios.isAxiosError(err)) {
    const data = err.response?.data as ApiErrorBody | undefined;
    if (data?.error?.message) return data.error.message;
    if (err.message) return err.message;
  }
  if (err instanceof Error) return err.message;
  return "알 수 없는 오류가 발생했습니다.";
}
