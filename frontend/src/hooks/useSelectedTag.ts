import { getTagDetail } from "../api/tags";
import type { TagDetail } from "../types/tag";
import { useAsyncResource } from "./useAsyncResource";

export function useSelectedTag(tagNo: string | undefined) {
  const { data: detail, loading, error } = useAsyncResource<
    string,
    TagDetail | null
  >(tagNo, getTagDetail, null);

  return { detail, loading, error };
}
