import { useEffect, useRef, useState } from "react";
import { search } from "../../api/search";
import type { SearchHit } from "../../types/common";
import { extractErrorMessage } from "../../utils/error";

interface SearchBarProps {
  onSelectTag: (tagNo: string) => void;
  onSelectDocument: (documentNo: string) => void;
}

/**
 * 통합 검색 바.
 * 입력 디바운스(300ms) 후 결과를 드롭다운으로 표시하고,
 * tag/document 결과 클릭 시 부모 콜백으로 위임.
 */
function SearchBar({ onSelectTag, onSelectDocument }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [hits, setHits] = useState<SearchHit[]>([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!query.trim()) {
      setHits([]);
      setError(null);
      return;
    }
    const timer = window.setTimeout(async () => {
      setLoading(true);
      setError(null);
      try {
        const results = await search(query, 30);
        setHits(results);
      } catch (e) {
        setError(extractErrorMessage(e));
      } finally {
        setLoading(false);
      }
    }, 300);
    return () => window.clearTimeout(timer);
  }, [query]);

  // 바깥 클릭 시 결과 닫기
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  function selectHit(hit: SearchHit) {
    setOpen(false);
    setQuery("");
    if (hit.hitType === "tag") onSelectTag(hit.key);
    else if (hit.hitType === "document") onSelectDocument(hit.key);
  }

  return (
    <div className="search-bar" ref={containerRef}>
      <input
        type="text"
        placeholder="Tag / System / Package / Document 검색"
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
      />
      {open && query.trim() && (
        <div className="search-results">
          {loading && <div className="search-results__empty">검색 중...</div>}
          {!loading && error && (
            <div className="search-results__empty status-block--error">{error}</div>
          )}
          {!loading && !error && hits.length === 0 && (
            <div className="search-results__empty">결과가 없습니다.</div>
          )}
          {!loading &&
            !error &&
            hits.map((hit) => (
              <div
                key={`${hit.hitType}-${hit.key}`}
                className="search-results__item"
                onClick={() => selectHit(hit)}
              >
                <span className="search-results__type">{hit.hitType}</span>
                <span>{hit.label}</span>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}

export default SearchBar;
