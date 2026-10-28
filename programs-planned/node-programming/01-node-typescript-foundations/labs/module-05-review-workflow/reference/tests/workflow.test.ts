import test from 'node:test';
import assert from 'node:assert/strict';
import { approve, reject, renderReview, submit, type Draft } from '../src/index.js';

const draft: Draft = { state: 'draft', text: 'A document', author: 'Ada' };

test('performs legal state transitions', () => {
  const reviewing = submit(draft, 'Grace', '2026-08-09T08:00:00.000Z');
  const approved = approve(reviewing, '2026-08-09T09:00:00.000Z');
  assert.equal(approved.state, 'approved');
  assert.equal(renderReview(approved), 'approved\tGrace\t2026-08-09T09:00:00.000Z');
});

test('requires rejection reason', () => {
  const reviewing = submit(draft, 'Grace', '2026-08-09T08:00:00.000Z');
  assert.throws(() => reject(reviewing, '2026-08-09T09:00:00.000Z', ' '));
});
