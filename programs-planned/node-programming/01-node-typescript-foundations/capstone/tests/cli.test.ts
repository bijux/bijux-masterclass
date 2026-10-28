import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';

interface ProcessResult { readonly code: number | null; readonly stdout: string; readonly stderr: string }
const main = fileURLToPath(new URL('../src/main.js', import.meta.url));

function runCli(dataPath: string, args: readonly string[]): Promise<ProcessResult> {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [main, ...args], {
      env: { ...process.env, STUDY_LEDGER_FILE: dataPath },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let stdout = '';
    let stderr = '';
    child.stdout.setEncoding('utf8');
    child.stderr.setEncoding('utf8');
    child.stdout.on('data', (chunk: string) => { stdout += chunk; });
    child.stderr.on('data', (chunk: string) => { stderr += chunk; });
    child.once('error', reject);
    child.once('close', (code) => resolve({ code, stdout, stderr }));
  });
}

test('the real process supports a complete session lifecycle', async () => {
  const root = await mkdtemp(join(tmpdir(), 'studyledger-cli-'));
  const dataPath = join(root, 'ledger.json');
  const planned = await runCli(dataPath, ['plan', '--topic', 'TypeScript unions', '--minutes', '35']);
  assert.equal(planned.code, 0);
  assert.equal(planned.stderr, '');
  assert.match(planned.stdout, /^planned\t1/u);

  assert.equal((await runCli(dataPath, ['start', '1'])).code, 0);
  assert.equal((await runCli(dataPath, ['complete', '1', '--minutes', '32', '--note', 'exhaustive switch'])).code, 0);
  const summary = await runCli(dataPath, ['summary']);
  assert.equal(summary.code, 0);
  assert.match(summary.stdout, /completed\t1/u);
  assert.match(summary.stdout, /completed-minutes\t32/u);
});

test('usage errors use exit status 2 and do not write the ledger', async () => {
  const root = await mkdtemp(join(tmpdir(), 'studyledger-cli-'));
  const dataPath = join(root, 'ledger.json');
  const result = await runCli(dataPath, ['plan', '--topic', 'Missing minutes']);
  assert.equal(result.code, 2);
  assert.match(result.stderr, /COMMAND_INVALID/u);
  const summary = await runCli(dataPath, ['summary']);
  assert.match(summary.stdout, /total\t0/u);
});
