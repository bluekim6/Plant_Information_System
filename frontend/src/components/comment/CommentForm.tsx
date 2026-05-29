import { useState } from "react";

interface CommentFormProps {
  /** 작성자 기본값 (Header 의 역할 select 와 연동될 수 있음). */
  defaultAuthor?: string;
  onSubmit: (content: string, author: string) => Promise<void>;
}

/**
 * Comment 입력 폼 (작성자 + 본문).
 *
 * 비즈니스 로직(생성 호출)은 부모(CommentPanel)에 위임. 이 컴포넌트는
 * 입력 검증 + UI 상태(작성 중/제출 중/오류)만 담당한다.
 */
function CommentForm({ defaultAuthor = "", onSubmit }: CommentFormProps) {
  const [content, setContent] = useState("");
  const [author, setAuthor] = useState(defaultAuthor);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!content.trim() || !author.trim()) return;
    setSubmitting(true);
    setError(null);
    try {
      await onSubmit(content.trim(), author.trim());
      setContent("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "등록 실패");
    } finally {
      setSubmitting(false);
    }
  }

  const canSubmit = !!content.trim() && !!author.trim() && !submitting;

  return (
    <form className="comment-form" onSubmit={handleSubmit}>
      <input
        className="comment-form__author"
        type="text"
        placeholder="작성자"
        value={author}
        onChange={(e) => setAuthor(e.target.value)}
      />
      <textarea
        className="comment-form__content"
        placeholder="Comment 내용을 입력하세요"
        rows={3}
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      {error && <div className="status-block status-block--error">{error}</div>}
      <div className="comment-form__actions">
        <button type="submit" disabled={!canSubmit}>
          {submitting ? "등록 중..." : "등록"}
        </button>
      </div>
    </form>
  );
}

export default CommentForm;
