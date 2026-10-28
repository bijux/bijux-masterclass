import type { Writable } from 'node:stream';
import { UsageError } from './errors.js';
import { inspectFile, runDemo, runFile } from './app.js';
import type { FailurePolicy } from './domain.js';

export interface CliEnvironment { readonly stdout: Pick<Writable, 'write'>; readonly stderr: Pick<Writable, 'write'>; readonly signal?: AbortSignal; }
const HELP = `TaskHarbor

Commands:
  inspect <manifest.json>
  run <manifest.json> [--concurrency <n>] [--policy continue|fail-fast] [--timeout-ms <n>]
  demo
  help
  version
`;

function positiveInteger(text: string | undefined, name: string): number {
  if (text === undefined || !/^[1-9][0-9]*$/u.test(text)) throw new UsageError(`${name} requires a positive integer`);
  return Number(text);
}

export async function runCli(args: readonly string[], environment: CliEnvironment): Promise<number> {
  const [command, ...rest] = args;
  if (command === undefined || command === 'help' || command === '--help' || command === '-h') { environment.stdout.write(HELP); return 0; }
  if (command === 'version' || command === '--version') { environment.stdout.write('taskharbor 1.0.0\n'); return 0; }
  if (command === 'inspect') {
    if (rest.length !== 1) throw new UsageError('inspect requires one manifest path');
    environment.stdout.write(await inspectFile(rest[0]!)); return 0;
  }
  if (command === 'demo') {
    if (rest.length !== 0) throw new UsageError('demo accepts no arguments');
    const options = environment.signal === undefined
      ? { concurrency: 2, policy: 'continue' as const }
      : { concurrency: 2, policy: 'continue' as const, signal: environment.signal };
    environment.stdout.write(await runDemo(options)); return 0;
  }
  if (command === 'run') {
    const path = rest[0]; if (!path) throw new UsageError('run requires a manifest path');
    let concurrency = 2; let policy: FailurePolicy = 'continue'; let timeoutMs: number | undefined;
    for (let index = 1; index < rest.length; index += 1) {
      const token = rest[index];
      if (token === '--concurrency') { concurrency = positiveInteger(rest[++index], '--concurrency'); continue; }
      if (token === '--timeout-ms') { timeoutMs = positiveInteger(rest[++index], '--timeout-ms'); continue; }
      if (token === '--policy') {
        const value = rest[++index];
        if (value !== 'continue' && value !== 'fail-fast') throw new UsageError('--policy must be continue or fail-fast');
        policy = value; continue;
      }
      throw new UsageError(`unknown option: ${token}`);
    }
    const base = environment.signal === undefined
      ? { concurrency, policy }
      : { concurrency, policy, signal: environment.signal };
    const result = timeoutMs === undefined ? await runFile(path, base) : await runFile(path, { ...base, timeoutMs });
    environment.stdout.write(result.text); return result.success ? 0 : 1;
  }
  environment.stderr.write(`unknown command: ${command}\n`);
  environment.stderr.write(HELP); return 2;
}
