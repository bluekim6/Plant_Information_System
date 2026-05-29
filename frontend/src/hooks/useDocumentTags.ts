import { useEffect, useState } from "react";
import { getDocumentTags } from "../api/documents";
import type { TagSummary } from "../types/common";
import { extractErrorMessage } from "../utils/error";

/**
 * 특정 도면이 포함하는 Tag 목록을 조회한다.
 *
 * documentNo 가 undefined 이면 fetch 하지 않음 (트리에서 펼치지 않은 도면용).
 */
export function useDocumentTags(documentNo: string | undefined) {
  const [tags, setTags] = useState<TagSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!documentNo) {
      setTags([]);
      setError(null);
      return;
    }
    setLoading(true);
    setError(null);
    let cancelled = false;
    getDocumentTags(documentNo)
      .then((t) => {
        if (!cancelled) setTags(t);
      })
      .catch((e) => {
        if (!cancelled) setError(extractErrorMessage(e));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [documentNo]);

  return { tags, loading, error };
}
