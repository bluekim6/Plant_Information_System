import apiClient from "./client";
import type {
  Comment,
  CommentCreate,
  CommentStatusChange,
  CommentUpdate,
} from "../types/comment";

/** Tag 의 Comment 목록 (오래된 순) */
export async function listCommentsByTag(tagNo: string): Promise<Comment[]> {
  const { data } = await apiClient.get<Comment[]>(
    `/api/tags/${encodeURIComponent(tagNo)}/comments`,
  );
  return data;
}

/** Comment 생성 */
export async function createComment(
  tagNo: string,
  body: CommentCreate,
): Promise<Comment> {
  const { data } = await apiClient.post<Comment>(
    `/api/tags/${encodeURIComponent(tagNo)}/comments`,
    body,
  );
  return data;
}

/** Comment 본문/연결 문서 수정 */
export async function updateComment(
  commentId: string,
  body: CommentUpdate,
): Promise<Comment> {
  const { data } = await apiClient.patch<Comment>(
    `/api/comments/${commentId}`,
    body,
  );
  return data;
}

/** Comment 상태 전이 (Open / Review / Closed) */
export async function changeCommentStatus(
  commentId: string,
  body: CommentStatusChange,
): Promise<Comment> {
  const { data } = await apiClient.patch<Comment>(
    `/api/comments/${commentId}/status`,
    body,
  );
  return data;
}

/** Comment 삭제 */
export async function deleteComment(
  commentId: string,
  author: string,
): Promise<void> {
  await apiClient.delete(`/api/comments/${commentId}`, {
    params: { author },
  });
}
