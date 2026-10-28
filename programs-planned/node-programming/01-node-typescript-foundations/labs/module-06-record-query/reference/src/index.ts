interface BaseRecord {
  readonly id: number;
  readonly title: string;
  readonly author: string;
  readonly year: number;
  readonly tags: readonly string[];
}
export interface DraftRecord extends BaseRecord { readonly state: 'draft' }
export interface PublishedRecord extends BaseRecord { readonly state: 'published'; readonly publishedAt: string }
export type RecordItem = DraftRecord | PublishedRecord;

export class DuplicateKeyError extends Error {
  override readonly name = 'DuplicateKeyError';
  constructor(readonly key: unknown, readonly firstIndex: number, readonly duplicateIndex: number) {
    super(`duplicate key ${String(key)} at positions ${firstIndex} and ${duplicateIndex}`);
  }
}

export function indexUniqueBy<T, Key>(values: readonly T[], keyOf: (value: T) => Key): Map<Key, T> {
  const result = new Map<Key, { readonly value: T; readonly index: number }>();
  for (let index = 0; index < values.length; index += 1) {
    const value = values[index];
    if (value === undefined) throw new Error('index invariant failed');
    const key = keyOf(value);
    const existing = result.get(key);
    if (existing !== undefined) throw new DuplicateKeyError(key, existing.index, index);
    result.set(key, { value, index });
  }
  return new Map([...result].map(([key, entry]) => [key, entry.value]));
}

export function groupBy<T, Key>(values: readonly T[], keyOf: (value: T) => Key): Map<Key, T[]> {
  const groups = new Map<Key, T[]>();
  for (const value of values) {
    const key = keyOf(value);
    const group = groups.get(key);
    if (group === undefined) groups.set(key, [value]);
    else group.push(value);
  }
  return groups;
}

export function isPublished(record: RecordItem): record is PublishedRecord {
  return record.state === 'published';
}

export function published(records: readonly RecordItem[]): PublishedRecord[] {
  return records.filter(isPublished);
}

export function searchTitles(records: readonly RecordItem[], rawQuery: string): RecordItem[] {
  const query = rawQuery.trim().toLocaleLowerCase('en-US');
  if (query === '') throw new Error('query must not be empty');
  return records
    .filter((record) => record.title.toLocaleLowerCase('en-US').includes(query))
    .slice()
    .sort((left, right) => left.id - right.id);
}
