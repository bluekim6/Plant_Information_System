import type { TagSummary } from "./common";

/** Tag 상세 — 백엔드 TagDetail 과 대응. attributes 는 원본 컬럼명 키 유지. */
export interface TagDetail extends TagSummary {
  referenceDrawing?: string | null;
  attributes: Record<string, string>;
}
