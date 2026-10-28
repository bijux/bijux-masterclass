import assert from 'node:assert/strict';
import test from 'node:test';
import { object, string } from '../src/index.js';
import { canonicalJson, parseJsonWith } from '../src/json.js';

test('JSON helpers keep syntax parsing and schema validation separate', () => {
  const Value = object({ name: string() });
  assert.deepEqual({ ...parseJsonWith(Value, '{"name":"Ada"}', 'user.json') }, { name: 'Ada' });
  assert.throws(() => parseJsonWith(Value, '{', 'broken.json'), /broken.json/);
  assert.equal(canonicalJson({ z: 1, a: { y: 2, b: 3 } }), '{\n  "a": {\n    "b": 3,\n    "y": 2\n  },\n  "z": 1\n}\n');
});
