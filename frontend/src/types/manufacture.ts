/** 제조사 상세 — 백엔드 ManufactureDetail 과 대응 */
export interface ManufactureDetail {
  id?: string | null;
  companyName: string;
  industrySector?: string | null;
  countryOrigin?: string | null;
  vendorCode?: string | null;
  phoneNumber?: string | null;
}
