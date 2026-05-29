import { useState } from "react";
import DocumentDetailPanel from "../components/document/DocumentDetailPanel";
import RelatedDocuments from "../components/document/RelatedDocuments";
import RelatedDocumentList from "../components/document/RelatedDocumentList";
import Header from "../components/layout/Header";
import Sidebar from "../components/layout/Sidebar";
import ManufactureModal from "../components/manufacture/ManufactureModal";
import TagDetailPanel from "../components/tag/TagDetailPanel";

type MainView = "tag-info" | "tag-documents" | "document-detail";

function MainPage() {
  const [currentTagNo, setCurrentTagNo] = useState<string>();
  const [currentDocumentNo, setCurrentDocumentNo] = useState<string>();
  const [currentView, setCurrentView] = useState<MainView>("tag-info");
  const [currentManufacture, setCurrentManufacture] = useState<string>();

  function selectTag(tagNo: string) {
    setCurrentTagNo(tagNo);
    setCurrentView("tag-info");
  }

  function showTagDocuments(tagNo: string) {
    setCurrentTagNo(tagNo);
    setCurrentView("tag-documents");
  }

  function selectDocument(documentNo: string) {
    setCurrentDocumentNo(documentNo);
    setCurrentView("document-detail");
  }

  function closeDocumentDetail() {
    if (currentTagNo) {
      setCurrentView("tag-info");
      return;
    }

    setCurrentDocumentNo(undefined);
  }

  return (
    <div className="app-shell">
      <Header onSelectTag={selectTag} onSelectDocument={selectDocument} />
      <div className="app-body">
        <Sidebar selectedTagNo={currentTagNo} onSelectTag={selectTag} />
        <div className="app-main">
          <main className="main-panel">
            <Breadcrumb
              view={currentView}
              tagNo={currentTagNo}
              documentNo={currentDocumentNo}
              onGoTag={() => setCurrentView("tag-info")}
              onGoTagDocuments={() => setCurrentView("tag-documents")}
            />

            {currentView === "tag-info" && (
              <TagDetailPanel
                tagNo={currentTagNo}
                onShowDocuments={showTagDocuments}
                onSelectManufacture={setCurrentManufacture}
                onSelectDocument={selectDocument}
              />
            )}

            {currentView === "tag-documents" && currentTagNo && (
              <RelatedDocumentList
                tagNo={currentTagNo}
                onSelectDocument={selectDocument}
                onBack={() => setCurrentView("tag-info")}
              />
            )}

            {currentView === "document-detail" && currentDocumentNo && (
              <DocumentDetailPanel
                documentNo={currentDocumentNo}
                onClose={closeDocumentDetail}
                closeLabel={
                  currentTagNo ? `Back to Tag ${currentTagNo}` : "Close"
                }
              />
            )}
          </main>
          <aside className="detail-panel">
            <RelatedDocuments
              tagNo={currentTagNo}
              activeDocumentNo={currentDocumentNo}
              onSelectDocument={selectDocument}
              onSelectTag={selectTag}
            />
          </aside>
        </div>
      </div>

      {currentManufacture && (
        <ManufactureModal
          manufactureName={currentManufacture}
          onClose={() => setCurrentManufacture(undefined)}
        />
      )}
    </div>
  );
}

interface BreadcrumbProps {
  view: MainView;
  tagNo?: string;
  documentNo?: string;
  onGoTag: () => void;
  onGoTagDocuments: () => void;
}

function Breadcrumb({
  view,
  tagNo,
  documentNo,
  onGoTag,
  onGoTagDocuments,
}: BreadcrumbProps) {
  if (!tagNo && !documentNo) return null;

  return (
    <div className="breadcrumb">
      {tagNo &&
        (view === "tag-info" ? (
          <span className="breadcrumb__current">Tag {tagNo}</span>
        ) : (
          <button className="breadcrumb__item" onClick={onGoTag}>
            Tag {tagNo}
          </button>
        ))}
      {view === "tag-documents" && (
        <>
          <span className="breadcrumb__sep">/</span>
          <span className="breadcrumb__current">Related documents</span>
        </>
      )}
      {view === "document-detail" && (
        <>
          {tagNo && (
            <>
              <span className="breadcrumb__sep">/</span>
              <button className="breadcrumb__item" onClick={onGoTagDocuments}>
                Related documents
              </button>
            </>
          )}
          <span className="breadcrumb__sep">/</span>
          <span className="breadcrumb__current">Document {documentNo}</span>
        </>
      )}
    </div>
  );
}

export default MainPage;
