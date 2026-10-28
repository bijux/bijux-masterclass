import assert from 'node:assert/strict';
import test from 'node:test';
import { mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const cli = new URL('../src/main.js', import.meta.url);

function run(args: readonly string[]) {
  return spawnSync(process.execPath, [cli.pathname, ...args], { encoding: 'utf8' });
}

test('CLI checks and normalizes versioned projects', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'schemakit-'));
  const input = join(directory, 'v1.json');
  const output = join(directory, 'v2.json');
  await writeFile(input, '{"format":"SCHEMAKIT_PROJECT_V1","name":"Legacy"}', 'utf8');
  const checked = run(['check', input]);
  assert.equal(checked.status, 0, checked.stderr);
  assert.match(checked.stdout, /SCHEMAKIT_PROJECT_V1/);
  const normalized = run(['normalize', input, output]);
  assert.equal(normalized.status, 0, normalized.stderr);
  const value = JSON.parse(await readFile(output, 'utf8')) as { readonly format: string; readonly tags: readonly string[] };
  assert.equal(value.format, 'SCHEMAKIT_PROJECT_V2');
  assert.deepEqual(value.tags, []);
});

test('CLI returns a distinct usage failure', () => {
  const result = run(['unknown']);
  assert.equal(result.status, 2);
  assert.match(result.stderr, /invalid command/);
});
