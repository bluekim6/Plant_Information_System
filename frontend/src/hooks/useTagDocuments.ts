import { getTagDocuments } from "../api/tags";
import type { DocumentSummary } from "../types/document";
import { useAsyncResource } from "./useAsyncResource";

const EMPTY_DOCUMENTS: DocumentSummary[] = [];

export function useTagDocuments(tagNo: string | undefined) {
  const { data: documents, loading, error } = useAsyncResource<
    string,
    DocumentSummary[]
  >(tagNo, getTagDocuments, EMPTY_DOCUMENTS);

  return { documents, loading, error };
}
