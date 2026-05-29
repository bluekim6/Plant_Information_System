import { getDocumentDetail } from "../api/documents";
import type { DocumentDetail } from "../types/document";
import { useAsyncResource } from "./useAsyncResource";

export function useSelectedDocument(documentNo: string | undefined) {
  const { data: detail, loading, error } = useAsyncResource<
    string,
    DocumentDetail | null
  >(documentNo, getDocumentDetail, null);

  return { detail, loading, error };
}
