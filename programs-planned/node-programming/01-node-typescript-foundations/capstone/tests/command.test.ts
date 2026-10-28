import test from 'node:test';
import assert from 'node:assert/strict';
import { parseCommand } from '../src/index.js';

test('plan parses named options without coercing text accidentally', () => {
  assert.deepEqual(parseCommand(['plan', '--topic', 'Closures', '--minutes', '45']), {
    kind: 'plan', topic: 'Closures', minutes: 45,
  });
});

test('complete preserves the absence of an optional note', () => {
  assert.deepEqual(parseCommand(['complete', '7', '--minutes', '30']), {
    kind: 'complete', id: 7, minutes: 30,
  });
});

test('duplicate options are rejected instead of silently taking the last value', () => {
  assert.throws(
    () => parseCommand(['plan', '--topic', 'A', '--topic', 'B', '--minutes', '10']),
    /may appear only once/u,
  );
});

test('numeric parsing rejects signs, whitespace, zero, and decimals', () => {
  for (const raw of ['-1', '+1', ' 1', '0', '1.5']) {
    assert.throws(() => parseCommand(['start', raw]));
  }
});

test('list validates status vocabulary', () => {
  assert.throws(() => parseCommand(['list', '--status', 'finished']), /planned, active, completed, or abandoned/u);
});
