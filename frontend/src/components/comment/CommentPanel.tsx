import { useEffect, useState } from "react";
import {
  changeCommentStatus,
  createComment,
  listCommentsByTag,
} from "../../api/comments";
import type { Comment, CommentStatus } from "../../types/comment";
import { extractErrorMessage } from "../../utils/error";
import CommentForm from "./CommentForm";

interface CommentPanelProps {
  tagNo: string;
  /** 변경 발생 시 부모(HistoryPanel 등)가 새로고침할 수 있게 알린다. */
  onChanged?: () => void;
}

const STATUSES: CommentStatus[] = ["Open", "Review", "Closed"];

/**
 * Tag 별 Comment 목록 + 입력 + 상태 변경 UI.
 *
 * - Tag 가 바뀌면 자동으로 목록 재로드.
 * - 등록/상태 변경 후 onChanged 콜백 호출 → HistoryPanel 새로고침에 활용.
 */
function CommentPanel({ tagNo, onChanged }: CommentPanelProps) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function reload() {
    setLoading(true);
    setError(null);
    try {
      const list = await listCommentsByTag(tagNo);
      setComments(list);
    } catch (e) {
      setError(extractErrorMessage(e));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    reload();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tagNo]);

  async function handleCreate(content: string, author: string) {
    await createComment(tagNo, { content, author });
    await reload();
    onChanged?.();
  }

  async function handleStatusChange(c: Comment, status: CommentStatus) {
    if (c.status === status) return;
    const author = window.prompt(
      `상태를 ${c.status} → ${status} 로 변경합니다.\n작성자(이력 기록용):`,
      c.author,
    );
    if (!author) return;
    try {
      await changeCommentStatus(c.id, { status, author });
      await reload();
      onChanged?.();
    } catch (e) {
      alert(extractErrorMessage(e));
    }
  }

  return (
    <section className="comment-panel">
      <h3>Comments ({comments.length})</h3>
      <CommentForm onSubmit={handleCreate} />

      {loading && <div className="status-block">불러오는 중...</div>}
      {error && <div className="status-block status-block--error">{error}</div>}
      {!loading && !error && comments.length === 0 && (
        <div className="status-block">아직 작성된 Comment 가 없습니다.</div>
      )}
      {!loading && !error && comments.length > 0 && (
        <ul className="comment-list">
          {comments.map((c) => (
            <li key={c.id} className="comment-item">
              <div className="comment-item__header">
                <span className={`status-badge status-badge--${c.status.toLowerCase()}`}>
                  {c.status}
                </span>
                <span className="comment-item__author">{c.author}</span>
                <span className="comment-item__time">
                  {new Date(c.createdAt).toLocaleString()}
                </span>
                {c.linkedDocumentNo && (
                  <span className="comment-item__doc">
                    🔗 {c.linkedDocumentNo}
                  </span>
                )}
              </div>
              <div className="comment-item__content">{c.content}</div>
              <div className="comment-item__actions">
                <span style={{ fontSize: 11, color: "#6b7280" }}>상태 변경:</span>
                {STATUSES.map((s) => (
                  <button
                    key={s}
                    type="button"
                    className={
                      "comment-item__status-btn" +
                      (c.status === s ? " comment-item__status-btn--active" : "")
                    }
                    onClick={() => handleStatusChange(c, s)}
                    disabled={c.status === s}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default CommentPanel;
