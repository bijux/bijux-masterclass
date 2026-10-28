export function isSupportedMajor(major: number): boolean {
  return Number.isSafeInteger(major) && major >= 24;
}
