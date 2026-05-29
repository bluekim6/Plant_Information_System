/** 백엔드 SystemNode 와 1:1 대응 */
export interface SystemNode {
  systemName: string;
  packageCount: number;
}

/** 백엔드 PackageNode 와 1:1 대응 */
export interface PackageNode {
  packageName: string;
  systemName?: string | null;
  tagCount: number;
}

/** Tag 요약 (목록용) — 백엔드 TagSummary 와 대응 */
export interface TagSummary {
  tagNo: string;
  description?: string | null;
  systemName?: string | null;
  packageName?: string | null;
  manufactureName?: string | null;
}

/** 통합 검색 결과 1건 */
export interface SearchHit {
  hitType: "tag" | "package" | "system" | "document";
  key: string;
  label: string;
}

/** 통일 에러 응답 형식 (백엔드 ErrorResponse) */
export interface ApiErrorBody {
  error: {
    code: string;
    message: string;
  };
}
