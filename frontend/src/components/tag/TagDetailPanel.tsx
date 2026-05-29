import type { ReactNode } from "react";
import { useState } from "react";
import { useSelectedTag } from "../../hooks/useSelectedTag";
import { displayOrDash } from "../../utils/format";
import StatusBlock from "../common/StatusBlock";
import CommentPanel from "../comment/CommentPanel";
import HistoryPanel from "../history/HistoryPanel";

interface TagDetailPanelProps {
  tagNo?: string;
  onShowDocuments: (tagNo: string) => void;
  onSelectManufacture: (name: string) => void;
  onSelectDocument: (documentNo: string) => void;
}

const PRIMARY_ATTRIBUTE_KEYS = ["Attribute A", "Attribute B"];

function TagDetailPanel({
  tagNo,
  onShowDocuments,
  onSelectManufacture,
  onSelectDocument,
}: TagDetailPanelProps) {
  const { detail, loading, error } = useSelectedTag(tagNo);
  const [showAllAttributes, setShowAllAttributes] = useState(false);
  const [historyRefreshKey, setHistoryRefreshKey] = useState(0);

  if (!tagNo) {
    return <StatusBlock>Select a tag from the tree to view details.</StatusBlock>;
  }
  if (loading) return <StatusBlock>Loading tag details...</StatusBlock>;
  if (error) return <StatusBlock variant="error">{error}</StatusBlock>;
  if (!detail) return <StatusBlock>Tag details were not found.</StatusBlock>;

  const attributeKeys = Object.keys(detail.attributes ?? {});
  const primaryKeys = PRIMARY_ATTRIBUTE_KEYS.filter(
    (key) => key in detail.attributes,
  );
  const secondaryKeys = attributeKeys.filter(
    (key) => !primaryKeys.includes(key),
  );

  return (
    <div className="tag-detail">
      <button
        type="button"
        className="tag-detail__heading"
        onClick={() => onShowDocuments(detail.tagNo)}
        title="Open related documents for this tag"
      >
        <h2 style={{ margin: 0 }}>{detail.tagNo}</h2>
        <span className="tag-detail__heading-hint">View related documents</span>
      </button>
      <div className="tag-detail__subtitle">
        {displayOrDash(detail.description)}
      </div>

      <div className="datasheet">
        <DatasheetCell label="System">{displayOrDash(detail.systemName)}</DatasheetCell>
        <DatasheetCell label="Package">{displayOrDash(detail.packageName)}</DatasheetCell>
        <DatasheetCell label="Reference Drawing">
          {detail.referenceDrawing ? (
            <button
              className="tag-detail__action"
              onClick={() => onSelectDocument(detail.referenceDrawing!)}
            >
              {detail.referenceDrawing}
            </button>
          ) : (
            "-"
          )}
        </DatasheetCell>
        <DatasheetCell label="Manufacture Name">
          {detail.manufactureName ? (
            <button
              className="tag-detail__action"
              onClick={() => onSelectManufacture(detail.manufactureName!)}
            >
              {detail.manufactureName}
            </button>
          ) : (
            "-"
          )}
        </DatasheetCell>
        {primaryKeys.map((key) => (
          <DatasheetCell key={key} label={key}>
            {displayOrDash(detail.attributes[key])}
          </DatasheetCell>
        ))}
      </div>

      {secondaryKeys.length > 0 && (
        <div className="attribute-toggle">
          <button onClick={() => setShowAllAttributes((value) => !value)}>
            {showAllAttributes ? "Hide" : "Show"} additional attributes (
            {secondaryKeys.length})
          </button>
          {showAllAttributes && (
            <div className="datasheet datasheet--dense">
              {secondaryKeys.map((key) => (
                <DatasheetCell key={key} label={key}>
                  {displayOrDash(detail.attributes[key])}
                </DatasheetCell>
              ))}
            </div>
          )}
        </div>
      )}

      <CommentPanel
        tagNo={detail.tagNo}
        onChanged={() => setHistoryRefreshKey((key) => key + 1)}
      />
      <HistoryPanel tagNo={detail.tagNo} refreshKey={historyRefreshKey} />
    </div>
  );
}

interface DatasheetCellProps {
  label: string;
  children: ReactNode;
}

function DatasheetCell({ label, children }: DatasheetCellProps) {
  return (
    <div className="datasheet-cell">
      <div className="datasheet-cell__label">{label}</div>
      <div className="datasheet-cell__value">{children}</div>
    </div>
  );
}

export default TagDetailPanel;
