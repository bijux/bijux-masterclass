import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';

function run(args: readonly string[]): Promise<{code:number|null; stdout:string; stderr:string}> {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, ['dist/src/main.js', ...args], { cwd: process.cwd(), stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '', stderr = '';
    child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8');
    child.stdout.on('data', (chunk) => { stdout += chunk; });
    child.stderr.on('data', (chunk) => { stderr += chunk; });
    child.on('error', reject);
    child.on('close', (code) => resolve({ code, stdout, stderr }));
  });
}

test('help, version, and demo are real process contracts', async () => {
  const help = await run(['help']);
  assert.equal(help.code, 0);
  assert.match(help.stdout, /ServiceWire/);
  const version = await run(['version']);
  assert.equal(version.stdout, 'servicewire 1.0.0\n');
  const demo = await run(['demo']);
  assert.equal(demo.code, 0, demo.stderr);
  assert.match(demo.stdout, /shutdown accepted=2 succeeded=2/);
});
