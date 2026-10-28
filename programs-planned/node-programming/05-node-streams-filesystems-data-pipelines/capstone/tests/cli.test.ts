import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
async function run(args: readonly string[]) { const child = spawn(process.execPath, [new URL('../src/main.js', import.meta.url).pathname, ...args], { stdio: ['ignore', 'pipe', 'pipe'] }); let stdout = '', stderr = ''; child.stdout?.setEncoding('utf8').on('data', c => stdout += c); child.stderr?.setEncoding('utf8').on('data', c => stderr += c); const [code] = await once(child, 'close') as [
    number | null,
    NodeJS.Signals | null
]; return { code, stdout, stderr }; }
test('help and usage exit statuses are stable', async () => { const help = await run(['help']); assert.equal(help.code, 0); assert.match(help.stdout, /FlowLedger/); const bad = await run(['unknown']); assert.equal(bad.code, 2); });
test('inspect command emits deterministic JSON report', async () => { const dir = await mkdtemp(join(tmpdir(), 'flow-')); const input = join(dir, 'in'); await writeFile(input, '{"id":"1","timestamp":"2026-08-09T09:00:00.000Z","kind":"x","value":1}\n'); const result = await run(['inspect', input]); assert.equal(result.code, 0); const value = JSON.parse(result.stdout) as {
    records: number;
}; assert.equal(value.records, 1); });
