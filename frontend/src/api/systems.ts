import apiClient from "./client";
import type { PackageNode, SystemNode, TagSummary } from "../types/common";

/** 전체 System 목록 + 각 System 의 Package 수 */
export async function listSystems(): Promise<SystemNode[]> {
  const { data } = await apiClient.get<SystemNode[]>("/api/systems");
  return data;
}

/** 특정 System 하위 Package 목록 + 각 Package 의 Tag 수 */
export async function listPackagesBySystem(systemName: string): Promise<PackageNode[]> {
  const { data } = await apiClient.get<PackageNode[]>(
    `/api/systems/${encodeURIComponent(systemName)}/packages`,
  );
  return data;
}

/** 특정 Package 하위 Tag 요약 목록 */
export async function listTagsByPackage(packageName: string): Promise<TagSummary[]> {
  const { data } = await apiClient.get<TagSummary[]>(
    `/api/packages/${encodeURIComponent(packageName)}/tags`,
  );
  return data;
}
