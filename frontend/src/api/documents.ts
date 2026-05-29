import apiClient from "./client";
import type { TagSummary } from "../types/common";
import type { DocumentDetail } from "../types/document";

/** 문서 상세 조회 */
export async function getDocumentDetail(documentNo: string): Promise<DocumentDetail> {
  const { data } = await apiClient.get<DocumentDetail>(
    `/api/documents/${encodeURIComponent(documentNo)}`,
  );
  return data;
}

/** 문서가 포함하는 Tag 목록 (PRD 시나리오 D) */
export async function getDocumentTags(documentNo: string): Promise<TagSummary[]> {
  const { data } = await apiClient.get<TagSummary[]>(
    `/api/documents/${encodeURIComponent(documentNo)}/tags`,
  );
  return data;
}

/** PDF 인라인 미리보기 URL (object/iframe 임베드 / 새 창 열람용).
 *
 * 상대 경로를 반환한다. Vite dev server proxy 가 /api/* 를 백엔드(8000)로
 * 라우팅하므로 브라우저 입장에서는 same-origin 이 되어, cross-origin PDF
 * 임베드 차단 정책을 우회한다.
 */
export function buildDrawingUrl(documentNo: string): string {
  return `/api/drawings/${encodeURIComponent(documentNo)}`;
}

/** PDF 다운로드 URL. 백엔드가 attachment 응답하여 브라우저가 파일로 저장. */
export function buildDownloadUrl(documentNo: string): string {
  return `/api/drawings/${encodeURIComponent(documentNo)}/download`;
}
