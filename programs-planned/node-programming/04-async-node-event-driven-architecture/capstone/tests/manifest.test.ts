import test from 'node:test';
import assert from 'node:assert/strict';
import { parseManifest } from '../src/manifest.js';

test('manifest defaults dependency and priority policy', () => {
  const manifest = parseManifest({ version: 'TASK_HARBOR_V1', tasks: [{ id: 'a', kind: 'echo', text: 'x' }] });
  assert.deepEqual(manifest.tasks[0], { id: 'a', kind: 'echo', text: 'x', dependsOn: [], priority: 'normal' });
});

test('manifest rejects unknown fields and duplicate dependency entries', () => {
  assert.throws(() => parseManifest({ version: 'TASK_HARBOR_V1', tasks: [{ id: 'a', kind: 'echo', text: 'x', extra: true }] }), /unknown field/);
  assert.throws(() => parseManifest({ version: 'TASK_HARBOR_V1', tasks: [{ id: 'a', kind: 'echo', text: 'x', dependsOn: ['b', 'b'] }] }), /duplicate/);
});
