import test from 'node:test';
import assert from 'node:assert/strict';
import { parseConfigJson, validateConfig } from '../src/index.js';

test('constructs trusted configuration', () => {
  assert.deepEqual(validateConfig({ mode: 'scan', concurrency: 4, maxInputBytes: 100, logLevel: 'info' }), {
    ok: true, value: { mode: 'scan', concurrency: 4, maxInputBytes: 100, logLevel: 'info' },
  });
});

test('accumulates deterministic issues', () => {
  const result = validateConfig({ mode: 'rewrite', concurrency: 0, maxInputBytes: -1, logLevel: 'loud', typo: true });
  assert.equal(result.ok, false);
  if (!result.ok) assert.deepEqual(result.issues.map((i) => i.path), ['typo', 'concurrency', 'maxInputBytes', 'outputDirectory', 'logLevel']);
});

test('keeps syntax failure separate', () => assert.throws(() => parseConfigJson('{'), /not valid JSON/));
