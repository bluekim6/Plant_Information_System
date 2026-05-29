import apiClient from "./client";
import type { DocumentSummary } from "../types/document";
import type { TagDetail } from "../types/tag";

/** Tag 상세 조회 */
export async function getTagDetail(tagNo: string): Promise<TagDetail> {
  const { data } = await apiClient.get<TagDetail>(
    `/api/tags/${encodeURIComponent(tagNo)}`,
  );
  return data;
}

/** Tag 와 연관된 문서/도면 목록 */
export async function getTagDocuments(tagNo: string): Promise<DocumentSummary[]> {
  const { data } = await apiClient.get<DocumentSummary[]>(
    `/api/tags/${encodeURIComponent(tagNo)}/documents`,
  );
  return data;
}
