import apiClient from "./client";
import type { ManufactureDetail } from "../types/manufacture";

/** Manufacture Name(=Company_Name)으로 제조사 상세 조회 (popup 용) */
export async function getManufactureByName(
  manufactureName: string,
): Promise<ManufactureDetail> {
  const { data } = await apiClient.get<ManufactureDetail>(
    `/api/manufactures/${encodeURIComponent(manufactureName)}`,
  );
  return data;
}
