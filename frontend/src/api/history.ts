import apiClient from "./client";
import type { HistoryEntry } from "../types/history";

/** Tag 단위 변경 이력 (최신순) */
export async function listTagHistory(tagNo: string): Promise<HistoryEntry[]> {
  const { data } = await apiClient.get<HistoryEntry[]>(
    `/api/tags/${encodeURIComponent(tagNo)}/history`,
  );
  return data;
}

/** 특정 Comment 의 변경 이력 (최신순) */
export async function listCommentHistory(
  commentId: string,
): Promise<HistoryEntry[]> {
  const { data } = await apiClient.get<HistoryEntry[]>(
    `/api/comments/${commentId}/history`,
  );
  return data;
}
