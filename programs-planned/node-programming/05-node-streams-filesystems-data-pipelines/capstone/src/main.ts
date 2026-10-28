#!/usr/bin/env node
import { parseCommand } from './command.js';
import { execute } from './app.js';
import { FlowError, UsageError } from './errors.js';
const controller = new AbortController();
const stop = (name: string) => controller.abort(new Error(`received ${name}`));
const onInt = () => stop('SIGINT'), onTerm = () => stop('SIGTERM');
process.once('SIGINT', onInt);
process.once('SIGTERM', onTerm);
try {
    const output = await execute(parseCommand(process.argv.slice(2)), controller.signal);
    await new Promise<void>((resolve, reject) => process.stdout.write(output, error => error ? reject(error) : resolve()));
    process.exitCode = 0;
}
catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    await new Promise<void>(resolve => process.stderr.write(`${message}\n`, () => resolve()));
    process.exitCode = error instanceof UsageError ? 2 : error instanceof FlowError ? 1 : 1;
}
finally {
    process.removeListener('SIGINT', onInt);
    process.removeListener('SIGTERM', onTerm);
}
