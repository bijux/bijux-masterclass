const CALIBRATION = new Map<string, number>([['lab', 0.2], ['field', -0.1]]);
export function calibrationFor(profile: string): number {
  const value = CALIBRATION.get(profile);
  if (value === undefined) throw new Error(`unknown profile: ${profile}`);
  return value;
}
