import { buildDrawingUrl } from "../../api/documents";

interface PdfViewerProps {
  documentNo: string;
  height?: string;
}

/**
 * PDF 인라인 뷰어.
 *
 * iframe 대신 <object> 를 사용하는 이유:
 *  - 일부 브라우저(특히 최신 Chrome/Edge) 가 cross-origin PDF 를 iframe 안에서
 *    차단하지만 <object> 는 더 관대하게 동작.
 *  - data 가 로드되지 않으면 children 을 fallback 으로 렌더링하므로,
 *    PDF 표시 실패 시 사용자가 "새 창 열기" 로 우회할 수 있다.
 *
 * Vite proxy 와 함께 동작하여 데브 모드에서는 same-origin 으로 응답을 받는다.
 */
function PdfViewer({ documentNo, height = "75vh" }: PdfViewerProps) {
  const src = buildDrawingUrl(documentNo);
  return (
    <object
      data={src}
      type="application/pdf"
      className="pdf-viewer"
      style={{ height, width: "100%" }}
    >
      <div className="status-block">
        브라우저가 PDF 미리보기를 표시할 수 없습니다.
        <br />
        <a href={src} target="_blank" rel="noopener noreferrer">
          새 창에서 열어보기
        </a>
      </div>
    </object>
  );
}

export default PdfViewer;
