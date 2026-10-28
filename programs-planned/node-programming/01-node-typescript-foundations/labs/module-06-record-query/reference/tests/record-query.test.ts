import test from 'node:test';
import assert from 'node:assert/strict';
import { DuplicateKeyError, groupBy, indexUniqueBy, published, searchTitles, type RecordItem } from '../src/index.js';

const records: readonly RecordItem[] = [
  { state: 'draft', id: 2, title: 'Type Models', author: 'Ada', year: 2026, tags: ['ts'] },
  { state: 'published', id: 1, title: 'Node Runtime', author: 'Ada', year: 2025, tags: ['node'], publishedAt: '2025-01-01T00:00:00.000Z' },
];

test('indexes unique values and reports positions', () => {
  assert.equal(indexUniqueBy(records, (r) => r.id).size, 2);
  assert.throws(() => indexUniqueBy([...records, records[0]!], (r) => r.id), (error: unknown) => {
    assert.ok(error instanceof DuplicateKeyError);
    assert.equal(error.firstIndex, 0);
    assert.equal(error.duplicateIndex, 2);
    return true;
  });
});

test('narrows published records', () => {
  assert.equal(published(records)[0]?.publishedAt, '2025-01-01T00:00:00.000Z');
});

test('search is deterministic and nonmutating', () => {
  const before = [...records];
  assert.deepEqual(searchTitles(records, 't'), [records[1], records[0]]);
  assert.deepEqual(records, before);
  assert.throws(() => searchTitles(records, '   '));
});

test('groups preserve source order', () => {
  assert.deepEqual(groupBy(records, (r) => r.author).get('Ada'), records);
});
