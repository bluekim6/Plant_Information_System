/** 변경 이력 액션 종류 */
export type HistoryAction = "created" | "updated" | "status_changed" | "deleted";

/** 백엔드 HistoryEntry 와 대응 */
export interface HistoryEntry {
  id: string;
  commentId?: string | null;
  tagNo: string;
  action: HistoryAction;
  author: string;
  timestamp: string; // ISO-8601
  before?: Record<string, unknown> | null;
  after?: Record<string, unknown> | null;
}
