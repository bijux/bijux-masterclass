import test from 'node:test';
import assert from 'node:assert/strict';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { inspectFile, runFile } from '../src/app.js';

const root = fileURLToPath(new URL('..', import.meta.url));
const fixture = join(root, '..', 'fixtures', 'demo.json');

test('inspect and run expose deterministic product text', async () => {
  const inspected = await inspectFile(fixture);
  assert.match(inspected, /topological: warmup -> message -> audit/);
  const run = await runFile(fixture, { concurrency: 2, policy: 'continue', runId: 'test-run' });
  assert.equal(run.success, true);
  assert.match(run.text, /message	succeeded	HARBOR/);
});
