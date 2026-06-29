import SearchBar from "../search/SearchBar";

/** PRD 9.1 사용자 역할 — 일단 화면 표시용으로만 사용. 권한 적용은 다음 단계. */
const USER_ROLES = [
  "설계 엔지니어",
  "Discipline Lead",
  "프로젝트 엔지니어",
  "문서관리 담당자",
  "검토/승인 담당자",
  "발주처 엔지니어",
  "운영 담당자",
  "유지보수 담당자",
];

interface HeaderProps {
  onSelectTag: (tagNo: string) => void;
  onSelectDocument: (documentNo: string) => void;
}

/** 시스템명 + 검색창 + 사용자 역할 표시 */
function Header({ onSelectTag, onSelectDocument }: HeaderProps) {
  return (
    <header className="app-header">
      <div className="app-header__title">Plant Information System</div>
      <SearchBar onSelectTag={onSelectTag} onSelectDocument={onSelectDocument} />
      <div className="app-header__role">
        <span>역할</span>
        <select defaultValue="설계 엔지니어">
          {USER_ROLES.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
      </div>
    </header>
  );
}

export default Header;
