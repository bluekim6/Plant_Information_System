import type { TagSummary } from "../../types/common";
import { displayOrDash } from "../../utils/format";

interface RelatedTagListProps {
  tags: TagSummary[];
  onSelectTag: (tagNo: string) => void;
}

/**
 * Tag 요약 목록을 렌더링하는 presentational 컴포넌트.
 *
 * PRD 시나리오 D:
 *   "그리고 그 도면이 가지고 있는 Tag 의 리스트를 화면에 표시 해 준다.
 *    다시 Tag 를 클릭하면 Tag 가 들고 있는 정보를 표시해주는 화면으로 돌아 온다."
 *
 * 데이터 fetch 는 부모(DocumentDetailPanel) 가 담당하고, 이 컴포넌트는 표시만 한다.
 */
function RelatedTagList({ tags, onSelectTag }: RelatedTagListProps) {
  if (tags.length === 0) {
    return <div className="status-block">연결된 Tag 가 없습니다.</div>;
  }
  return (
    <ul className="doc-list">
      {tags.map((t) => (
        <li key={t.tagNo}>
          <button
            className="doc-list__no tag-detail__action"
            style={{ textDecoration: "none", padding: 0 }}
            onClick={() => onSelectTag(t.tagNo)}
          >
            {t.tagNo}
          </button>
          <div className="doc-list__meta">
            {displayOrDash(t.description)} · {displayOrDash(t.systemName)} /{" "}
            {displayOrDash(t.packageName)}
          </div>
        </li>
      ))}
    </ul>
  );
}

export default RelatedTagList;
