export interface RecordItem {
  readonly id: number;
  readonly title: string;
}

export function titles(records: readonly RecordItem[]): string[] {
  return records.map((record) => record.title);
}
