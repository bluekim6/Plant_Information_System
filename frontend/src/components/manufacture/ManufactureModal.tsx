import { useEffect, useState } from "react";
import { getManufactureByName } from "../../api/manufactures";
import type { ManufactureDetail } from "../../types/manufacture";
import { displayOrDash } from "../../utils/format";
import { extractErrorMessage } from "../../utils/error";

interface ManufactureModalProps {
  manufactureName: string;
  onClose: () => void;
}

/**
 * 제조사 상세 모달.
 * PRD 시나리오 D: Tag 화면에서 Manufacture Name 클릭 시 popup 으로 표시.
 */
function ManufactureModal({ manufactureName, onClose }: ManufactureModalProps) {
  const [detail, setDetail] = useState<ManufactureDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getManufactureByName(manufactureName)
      .then(setDetail)
      .catch((e) => setError(extractErrorMessage(e)))
      .finally(() => setLoading(false));
  }, [manufactureName]);

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal__header">
          <h3>제조사 정보</h3>
          <button className="modal__close" onClick={onClose} aria-label="close">
            ×
          </button>
        </div>
        <div className="modal__body">
          {loading && <div className="status-block">불러오는 중...</div>}
          {error && <div className="status-block status-block--error">{error}</div>}
          {!loading && !error && detail && (
            <dl className="tag-detail__grid">
              <dt>Company Name</dt>
              <dd>{detail.companyName}</dd>
              <dt>ID</dt>
              <dd>{displayOrDash(detail.id)}</dd>
              <dt>Company Type</dt>
              <dd>{displayOrDash(detail.companyType)}</dd>
              <dt>Address</dt>
              <dd>{displayOrDash(detail.address)}</dd>
              <dt>Town</dt>
              <dd>{displayOrDash(detail.town)}</dd>
              <dt>Province</dt>
              <dd>{displayOrDash(detail.province)}</dd>
              <dt>Phone</dt>
              <dd>{displayOrDash(detail.phoneNumber)}</dd>
              <dt>E-mail</dt>
              <dd>{displayOrDash(detail.email)}</dd>
              <dt>Website</dt>
              <dd>{displayOrDash(detail.website)}</dd>
              <dt>Contact Person</dt>
              <dd>{displayOrDash(detail.contactPerson)}</dd>
            </dl>
          )}
        </div>
      </div>
    </div>
  );
}

export default ManufactureModal;
