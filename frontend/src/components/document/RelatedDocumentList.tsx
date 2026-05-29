import { useTagDocuments } from "../../hooks/useTagDocuments";
import { displayOrDash } from "../../utils/format";
import StatusBlock from "../common/StatusBlock";

interface RelatedDocumentListProps {
  tagNo: string;
  onSelectDocument: (documentNo: string) => void;
  onBack: () => void;
}

function RelatedDocumentList({
  tagNo,
  onSelectDocument,
  onBack,
}: RelatedDocumentListProps) {
  const { documents, loading, error } = useTagDocuments(tagNo);

  return (
    <div className="tag-detail">
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <button className="tag-detail__action" onClick={onBack}>
          Back to Tag {tagNo}
        </button>
      </div>
      <h2 style={{ marginTop: 8 }}>Related documents for Tag {tagNo}</h2>
      <div className="tag-detail__subtitle">
        Select a document number to open its detail view.
      </div>

      {loading && <StatusBlock>Loading related documents...</StatusBlock>}
      {error && <StatusBlock variant="error">{error}</StatusBlock>}
      {!loading && !error && documents.length === 0 && (
        <StatusBlock>No related documents found for this tag.</StatusBlock>
      )}
      {!loading && !error && documents.length > 0 && (
        <ul className="doc-list">
          {documents.map((document) => (
            <li key={document.documentNo}>
              <button
                className="doc-list__no tag-detail__action"
                style={{ textDecoration: "none", padding: 0, fontSize: 15 }}
                onClick={() => onSelectDocument(document.documentNo)}
              >
                {document.documentNo}
              </button>
              <div className="doc-list__meta">
                {displayOrDash(document.documentName)} | Rev{" "}
                {displayOrDash(document.revision)}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default RelatedDocumentList;
