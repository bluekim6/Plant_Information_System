/** 빈 문자열/undefined 를 표시용 placeholder 로 치환한다. */
export function displayOrDash(value?: string | null): string {
  if (value === undefined || value === null || value === "") return "-";
  return value;
}
