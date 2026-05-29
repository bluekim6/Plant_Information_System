/** Comment 상태 (PRD 9.3) */
export type CommentStatus = "Open" | "Review" | "Closed";

/** 백엔드 Comment 모델과 1:1 대응 */
export interface Comment {
  id: string;
  tagNo: string;
  content: string;
  author: string;
  status: CommentStatus;
  linkedDocumentNo?: string | null;
  createdAt: string; // ISO-8601
  updatedAt: string;
}

/** Comment 생성 요청 body */
export interface CommentCreate {
  content: string;
  author: string;
  linkedDocumentNo?: string | null;
}

/** 본문/연결 문서 수정 */
export interface CommentUpdate {
  content?: string;
  linkedDocumentNo?: string | null;
  author: string;
}

/** 상태 전이 */
export interface CommentStatusChange {
  status: CommentStatus;
  author: string;
}
