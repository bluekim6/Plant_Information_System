import { useEffect, useState } from "react";
import {
  listPackagesBySystem,
  listSystems,
  listTagsByPackage,
} from "../../api/systems";
import type { PackageNode, SystemNode, TagSummary } from "../../types/common";
import { extractErrorMessage } from "../../utils/error";

interface SystemTreeProps {
  selectedTagNo?: string;
  onSelectTag: (tagNo: string) => void;
}

/**
 * 좌측 사이드바 트리.
 * - 첫 진입 시 System 목록만 로드
 * - System 토글 시 해당 System 의 Package 를 lazy load
 * - Package 토글 시 해당 Package 의 Tag 를 lazy load
 *
 * 데이터 fetch 는 이 컴포넌트 안에 캡슐화하되 모두 api/systems 모듈에 위임한다.
 */
function SystemTree({ selectedTagNo, onSelectTag }: SystemTreeProps) {
  const [systems, setSystems] = useState<SystemNode[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 펼친 시스템/패키지 키와 해당 자식들 캐시
  const [openSystems, setOpenSystems] = useState<Record<string, PackageNode[] | "loading" | "error">>({});
  const [openPackages, setOpenPackages] = useState<Record<string, TagSummary[] | "loading" | "error">>({});

  useEffect(() => {
    setLoading(true);
    listSystems()
      .then(setSystems)
      .catch((e) => setError(extractErrorMessage(e)))
      .finally(() => setLoading(false));
  }, []);

  async function toggleSystem(name: string) {
    if (openSystems[name] !== undefined) {
      // 이미 열려 있으면 닫기
      const next = { ...openSystems };
      delete next[name];
      setOpenSystems(next);
      return;
    }
    setOpenSystems((s) => ({ ...s, [name]: "loading" }));
    try {
      const pkgs = await listPackagesBySystem(name);
      setOpenSystems((s) => ({ ...s, [name]: pkgs }));
    } catch {
      setOpenSystems((s) => ({ ...s, [name]: "error" }));
    }
  }

  async function togglePackage(name: string) {
    if (openPackages[name] !== undefined) {
      const next = { ...openPackages };
      delete next[name];
      setOpenPackages(next);
      return;
    }
    setOpenPackages((p) => ({ ...p, [name]: "loading" }));
    try {
      const tags = await listTagsByPackage(name);
      setOpenPackages((p) => ({ ...p, [name]: tags }));
    } catch {
      setOpenPackages((p) => ({ ...p, [name]: "error" }));
    }
  }

  if (loading) return <div className="status-block">시스템 목록 불러오는 중...</div>;
  if (error) return <div className="status-block status-block--error">{error}</div>;
  if (systems.length === 0) return <div className="status-block">표시할 System 이 없습니다.</div>;

  return (
    <div className="tree-section">
      <div className="tree-section__title">System / Package / Tag</div>
      {systems.map((sys) => {
        const sysState = openSystems[sys.systemName];
        const isOpen = sysState !== undefined;
        return (
          <div className="tree-node" key={sys.systemName}>
            <div className="tree-node__row" onClick={() => toggleSystem(sys.systemName)}>
              <span className="tree-node__caret">{isOpen ? "▾" : "▸"}</span>
              <span>{sys.systemName}</span>
              <span className="tree-node__count">{sys.packageCount}</span>
            </div>
            {isOpen && (
              <div className="tree-children">
                {sysState === "loading" && (
                  <div className="status-block">패키지 불러오는 중...</div>
                )}
                {sysState === "error" && (
                  <div className="status-block status-block--error">패키지 로드 실패</div>
                )}
                {Array.isArray(sysState) &&
                  sysState.map((pkg) => {
                    const pkgState = openPackages[pkg.packageName];
                    const pkgOpen = pkgState !== undefined;
                    return (
                      <div className="tree-node" key={pkg.packageName}>
                        <div
                          className="tree-node__row"
                          onClick={() => togglePackage(pkg.packageName)}
                        >
                          <span className="tree-node__caret">{pkgOpen ? "▾" : "▸"}</span>
                          <span>{pkg.packageName}</span>
                          <span className="tree-node__count">{pkg.tagCount}</span>
                        </div>
                        {pkgOpen && (
                          <div className="tree-children">
                            {pkgState === "loading" && (
                              <div className="status-block">태그 불러오는 중...</div>
                            )}
                            {pkgState === "error" && (
                              <div className="status-block status-block--error">
                                태그 로드 실패
                              </div>
                            )}
                            {Array.isArray(pkgState) &&
                              pkgState.map((tag) => {
                                const isSelected = tag.tagNo === selectedTagNo;
                                return (
                                  <div
                                    key={tag.tagNo}
                                    className={
                                      "tree-node__row" +
                                      (isSelected ? " tree-node__row--selected" : "")
                                    }
                                    onClick={() => onSelectTag(tag.tagNo)}
                                  >
                                    <span className="tree-node__caret">·</span>
                                    <span>{tag.tagNo}</span>
                                  </div>
                                );
                              })}
                          </div>
                        )}
                      </div>
                    );
                  })}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default SystemTree;
