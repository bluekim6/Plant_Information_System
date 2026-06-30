/** 제조사 상세 — 백엔드 ManufactureDetail 과 대응 */
export interface ManufactureDetail {
  id?: string | null;
  companyName: string;
  address?: string | null;
  town?: string | null;
  province?: string | null;
  phoneNumber?: string | null;
  email?: string | null;
  website?: string | null;
  contactPerson?: string | null;
  companyType?: string | null;
}
