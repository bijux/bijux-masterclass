import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { join } from 'node:path';

const root = fileURLToPath(new URL('..', import.meta.url));
const cli = join(root, 'src', 'main.js');
const fixture = join(root, '..', 'fixtures', 'demo.json');

function execute(args: readonly string[]): Promise<{ code: number | null; stdout: string; stderr: string }> {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [cli, ...args], { stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = ''; let stderr = '';
    child.stdout.setEncoding('utf8').on('data', chunk => { stdout += chunk; });
    child.stderr.setEncoding('utf8').on('data', chunk => { stderr += chunk; });
    child.once('error', reject); child.once('close', code => resolve({ code, stdout, stderr }));
  });
}

test('real CLI reports version and executes a manifest', async () => {
  const version = await execute(['version']);
  assert.deepEqual(version, { code: 0, stdout: 'taskharbor 1.0.0\n', stderr: '' });
  const run = await execute(['run', fixture, '--concurrency', '2']);
  assert.equal(run.code, 0); assert.match(run.stdout, /totals: succeeded=3/); assert.equal(run.stderr, '');
});
