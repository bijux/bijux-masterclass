import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { gzipSync, gunzipSync } from 'node:zlib';
import { transformFile } from '../src/pipeline.js';
test('supports gzip input and output while hashing canonical bytes', async () => { const dir = await mkdtemp(join(tmpdir(), 'flow-')); const input = join(dir, 'in.gz'), out = join(dir, 'out.gz'); const line = '{"id":"1","timestamp":"2026-08-09T09:00:00.000Z","kind":"keep","value":1}\n'; await writeFile(input, gzipSync(line)); const report = await transformFile(input, out, { gzipInput: true, gzipOutput: true, replace: false }); assert.equal(gunzipSync(await readFile(out)).toString(), line); assert.equal(report.emitted, 1); });
