import { useEffect, useState } from "react";
import { extractErrorMessage } from "../utils/error";

interface AsyncResourceState<T> {
  data: T;
  loading: boolean;
  error: string | null;
}

export function useAsyncResource<TInput, TData>(
  input: TInput | undefined,
  fetcher: (input: TInput) => Promise<TData>,
  emptyValue: TData,
): AsyncResourceState<TData> {
  const [data, setData] = useState<TData>(emptyValue);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (input === undefined || input === null || input === "") {
      setData(emptyValue);
      setError(null);
      setLoading(false);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError(null);

    fetcher(input)
      .then((nextData) => {
        if (!cancelled) setData(nextData);
      })
      .catch((err) => {
        if (!cancelled) setError(extractErrorMessage(err));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [emptyValue, fetcher, input]);

  return { data, loading, error };
}
