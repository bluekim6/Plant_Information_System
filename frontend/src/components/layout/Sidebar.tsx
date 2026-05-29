import SystemTree from "../hierarchy/SystemTree";

interface SidebarProps {
  selectedTagNo?: string;
  onSelectTag: (tagNo: string) => void;
}

/** 좌측 사이드바 — 현재는 SystemTree 만 포함하지만, 향후 다른 트리/필터 추가 여지를 둠. */
function Sidebar({ selectedTagNo, onSelectTag }: SidebarProps) {
  return (
    <aside className="app-sidebar">
      <SystemTree selectedTagNo={selectedTagNo} onSelectTag={onSelectTag} />
    </aside>
  );
}

export default Sidebar;
