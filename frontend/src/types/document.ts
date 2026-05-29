/** 문서/도면 요약 — 백엔드 DocumentSummary 와 대응 */
export interface DocumentSummary {
  documentNo: string;
  documentName?: string | null;
  revision?: string | null;
}

/** 문서/도면 상세 — 백엔드 DocumentDetail 과 대응 */
export interface DocumentDetail extends DocumentSummary {
  pdfAvailable: boolean;
}
