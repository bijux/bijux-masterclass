#!/usr/bin/env node
import { runCli } from './cli.js';
import { UsageError, describeError } from './errors.js';

const controller = new AbortController();
let signalCount = 0;
const onSignal = (): void => {
  signalCount += 1;
  if (!controller.signal.aborted) controller.abort(new Error('process termination requested'));
  else if (signalCount > 1) process.exitCode = 130;
};
process.on('SIGINT', onSignal);
process.on('SIGTERM', onSignal);

try {
  process.exitCode = await runCli(process.argv.slice(2), { stdout: process.stdout, stderr: process.stderr, signal: controller.signal });
} catch (error) {
  process.stderr.write(`${describeError(error)}
`);
  process.exitCode = error instanceof UsageError ? 2 : 1;
} finally {
  process.off('SIGINT', onSignal);
  process.off('SIGTERM', onSignal);
}
