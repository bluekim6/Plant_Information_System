import { useEffect, useState } from "react";
import { listTagHistory } from "../../api/history";
import type { HistoryAction, HistoryEntry } from "../../types/history";
import { extractErrorMessage } from "../../utils/error";

interface HistoryPanelProps {
  tagNo: string;
  /** CommentPanel 의 변경마다 증가하는 카운터 등을 prop 으로 받아 자동 새로고침. */
  refreshKey?: number;
}

const ACTION_LABEL: Record<HistoryAction, string> = {
  created: "생성",
  updated: "수정",
  status_changed: "상태 변경",
  deleted: "삭제",
};

/**
 * Tag 단위 변경 이력 (최신순).
 * before/after 는 length 가 길어질 수 있어 details 토글로 제공.
 */
function HistoryPanel({ tagNo, refreshKey = 0 }: HistoryPanelProps) {
  const [entries, setEntries] = useState<HistoryEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    listTagHistory(tagNo)
      .then(setEntries)
      .catch((e) => setError(extractErrorMessage(e)))
      .finally(() => setLoading(false));
  }, [tagNo, refreshKey]);

  return (
    <section className="history-panel">
      <h3>변경 이력 ({entries.length})</h3>
      {loading && <div className="status-block">불러오는 중...</div>}
      {error && <div className="status-block status-block--error">{error}</div>}
      {!loading && !error && entries.length === 0 && (
        <div className="status-block">변경 이력이 없습니다.</div>
      )}
      {!loading && !error && entries.length > 0 && (
        <ul className="history-list">
          {entries.map((h) => (
            <li key={h.id} className="history-item">
              <div className="history-item__header">
                <span className={`history-action history-action--${h.action}`}>
                  {ACTION_LABEL[h.action]}
                </span>
                <span className="history-item__author">{h.author}</span>
                <span className="history-item__time">
                  {new Date(h.timestamp).toLocaleString()}
                </span>
              </div>
              {(h.before || h.after) && (
                <details className="history-item__diff">
                  <summary>변경 내용 보기</summary>
                  {h.before && (
                    <div>
                      <strong>Before:</strong>
                      <pre>{JSON.stringify(h.before, null, 2)}</pre>
                    </div>
                  )}
                  {h.after && (
                    <div>
                      <strong>After:</strong>
                      <pre>{JSON.stringify(h.after, null, 2)}</pre>
                    </div>
                  )}
                </details>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default HistoryPanel;
