#!/usr/bin/env node
import { executeCommand } from './app.js';
import { parseCommand, UsageError } from './command.js';
import { ServiceWireClientError } from './client.js';

const controller = new AbortController();
let signalCount = 0;
const onSignal = (name: string): void => {
  signalCount += 1;
  if (!controller.signal.aborted) controller.abort(new Error(`received ${name}`));
  else if (signalCount > 1) process.exitCode = 130;
};
const onInt = () => onSignal('SIGINT');
const onTerm = () => onSignal('SIGTERM');
process.on('SIGINT', onInt);
process.on('SIGTERM', onTerm);

try {
  const result = await executeCommand(parseCommand(process.argv.slice(2)), controller.signal);
  if (result.stdout.length > 0) {
    await new Promise<void>((resolve, reject) => {
      process.stdout.write(result.stdout, (error) => error ? reject(error) : resolve());
    });
  }
  process.exitCode = result.exitCode;
} catch (error) {
  const message = error instanceof Error ? `${error.name}: ${error.message}` : String(error);
  await new Promise<void>((resolve) => process.stderr.write(`${message}\n`, () => resolve()));
  process.exitCode = error instanceof UsageError ? 2 : error instanceof ServiceWireClientError ? 1 : 1;
} finally {
  process.off('SIGINT', onInt);
  process.off('SIGTERM', onTerm);
}
