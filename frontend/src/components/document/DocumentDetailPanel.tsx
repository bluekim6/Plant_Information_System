import { buildDownloadUrl, buildDrawingUrl } from "../../api/documents";
import { useSelectedDocument } from "../../hooks/useSelectedDocument";
import { displayOrDash } from "../../utils/format";
import StatusBlock from "../common/StatusBlock";
import PdfViewer from "./PdfViewer";

interface DocumentDetailPanelProps {
  documentNo: string;
  onClose: () => void;
  closeLabel?: string;
}

function DocumentDetailPanel({
  documentNo,
  onClose,
  closeLabel,
}: DocumentDetailPanelProps) {
  const { detail, loading, error } = useSelectedDocument(documentNo);

  return (
    <div className="tag-detail">
      <div className="document-detail__header">
        <h2 style={{ margin: 0 }}>{documentNo}</h2>
        {detail && (
          <span className="document-detail__meta">
            {displayOrDash(detail.documentName)} | Rev{" "}
            {displayOrDash(detail.revision)}
          </span>
        )}
        <div style={{ flex: 1 }} />
        {detail?.pdfAvailable && (
          <>
            <a
              className="tag-detail__action"
              href={buildDrawingUrl(documentNo)}
              target="_blank"
              rel="noopener noreferrer"
            >
              Open PDF
            </a>
            <a className="tag-detail__action" href={buildDownloadUrl(documentNo)}>
              Download
            </a>
          </>
        )}
        <button className="tag-detail__action" onClick={onClose}>
          {closeLabel ?? "Close"}
        </button>
      </div>

      {loading && <StatusBlock>Loading document...</StatusBlock>}
      {error && <StatusBlock variant="error">{error}</StatusBlock>}

      {!loading &&
        !error &&
        detail &&
        (detail.pdfAvailable ? (
          <PdfViewer documentNo={documentNo} />
        ) : (
          <StatusBlock>No PDF is available for this document.</StatusBlock>
        ))}
    </div>
  );
}

export default DocumentDetailPanel;
