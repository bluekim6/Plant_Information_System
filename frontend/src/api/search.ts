import apiClient from "./client";
import type { SearchHit } from "../types/common";

/** 통합 검색 — Tag/System/Package/Document 에서 부분 일치 검색 */
export async function search(query: string, limit = 30): Promise<SearchHit[]> {
  const { data } = await apiClient.get<SearchHit[]>("/api/search", {
    params: { q: query, limit },
  });
  return data;
}
