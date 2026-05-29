import { useEffect, useState } from "react";
import { useDocumentTags } from "../../hooks/useDocumentTags";
import { useTagDocuments } from "../../hooks/useTagDocuments";
import type { DocumentSummary } from "../../types/document";
import { displayOrDash } from "../../utils/format";

interface RelatedDocumentsProps {
  tagNo?: string;
  /** 현재 메인 영역에 표시 중인 도면 (있으면 트리에서 자동 펼침 + 강조). */
  activeDocumentNo?: string;
  onSelectDocument: (documentNo: string) => void;
  onSelectTag: (tagNo: string) => void;
}

/**
 * 우측 패널 — 관련 도면을 하이라키 트리로 표시.
 *
 *  관련 문서 / 도면
 *  ▾ ABCD-DE-6612          ← 현재 보고 있는 도면 (자동 펼침)
 *      ZDatasheet · Rev A
 *      ├ G-0318
 *      ├ G-0319
 *      └ ...
 *  ▸ ABCD-AL-6668          ← 클릭하면 펼쳐서 그 도면의 Tag 목록을 확인
 *      WDatasheet · Rev C
 */
function RelatedDocuments({
  tagNo,
  activeDocumentNo,
  onSelectDocument,
  onSelectTag,
}: RelatedDocumentsProps) {
  const { documents, loading, error } = useTagDocuments(tagNo);

  return (
    <section>
      <h3>관련 문서 / 도면</h3>
      {!tagNo && <div className="status-block">Tag 를 선택하면 표시됩니다.</div>}
      {tagNo && loading && <div className="status-block">불러오는 중...</div>}
      {tagNo && error && (
        <div className="status-block status-block--error">{error}</div>
      )}
      {tagNo && !loading && !error && documents.length === 0 && (
        <div className="status-block">연결된 문서가 없습니다.</div>
      )}
      {tagNo && !loading && !error && documents.length > 0 && (
        <ul className="doc-tree">
          {documents.map((d) => (
            <DocumentTreeItem
              key={d.documentNo}
              doc={d}
              isActive={d.documentNo === activeDocumentNo}
              onSelectDocument={onSelectDocument}
              onSelectTag={onSelectTag}
            />
          ))}
        </ul>
      )}
    </section>
  );
}

interface DocumentTreeItemProps {
  doc: DocumentSummary;
  isActive: boolean;
  onSelectDocument: (documentNo: string) => void;
  onSelectTag: (tagNo: string) => void;
}

/** 도면 한 개 + 펼치면 그 도면이 포함하는 Tag 목록. */
function DocumentTreeItem({
  doc,
  isActive,
  onSelectDocument,
  onSelectTag,
}: DocumentTreeItemProps) {
  // 사용자가 명시적으로 펼친 상태 (null = 미설정 → isActive 따라감)
  const [userExpanded, setUserExpanded] = useState<boolean | null>(null);
  // 활성 도면이 바뀌면 사용자 토글 초기화 → 자동 펼침에 맡김
  useEffect(() => {
    setUserExpanded(null);
  }, [isActive]);

  const expanded = userExpanded === null ? isActive : userExpanded;

  function toggle(e: React.MouseEvent) {
    e.stopPropagation();
    setUserExpanded(!expanded);
  }

  return (
    <li className={"doc-tree__item" + (isActive ? " doc-tree__item--active" : "")}>
      <div className="doc-tree__row">
        <button
          type="button"
          className="doc-tree__caret"
          onClick={toggle}
          aria-label={expanded ? "접기" : "펼치기"}
        >
          {expanded ? "▾" : "▸"}
        </button>
        <button
          type="button"
          className="doc-tree__doc-no"
          onClick={() => onSelectDocument(doc.documentNo)}
        >
          {doc.documentNo}
        </button>
      </div>
      <div className="doc-tree__meta">
        {displayOrDash(doc.documentName)} · Rev {displayOrDash(doc.revision)}
      </div>
      {expanded && (
        <DocumentTagBranch documentNo={doc.documentNo} onSelectTag={onSelectTag} />
      )}
    </li>
  );
}

interface DocumentTagBranchProps {
  documentNo: string;
  onSelectTag: (tagNo: string) => void;
}

/** 펼친 도면 아래에 표시되는 Tag 가지. */
function DocumentTagBranch({ documentNo, onSelectTag }: DocumentTagBranchProps) {
  const { tags, loading, error } = useDocumentTags(documentNo);

  if (loading) return <div className="doc-tree__branch-status">Tag 불러오는 중...</div>;
  if (error) return <div className="doc-tree__branch-status">{error}</div>;
  if (tags.length === 0) return <div className="doc-tree__branch-status">Tag 없음</div>;

  return (
    <ul className="doc-tree__tag-list">
      {tags.map((t) => (
        <li key={t.tagNo}>
          <button
            type="button"
            className="doc-tree__tag"
            onClick={() => onSelectTag(t.tagNo)}
            title={t.description ?? ""}
          >
            {t.tagNo}
          </button>
        </li>
      ))}
    </ul>
  );
}

export default RelatedDocuments;
