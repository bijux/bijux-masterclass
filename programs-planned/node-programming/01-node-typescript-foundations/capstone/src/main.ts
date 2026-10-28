#!/usr/bin/env node
import { homedir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { executeCommand } from './app.js';
import { parseCommand } from './command.js';
import { CommandError, StudyLedgerError } from './errors.js';
import { renderError, renderHelp } from './render.js';
import { loadLedger, saveLedger } from './storage.js';

export interface ProcessLike {
  readonly argv: readonly string[];
  readonly env: NodeJS.ProcessEnv;
  readonly stdout: { write(text: string): unknown };
  readonly stderr: { write(text: string): unknown };
}

function dataPath(environment: NodeJS.ProcessEnv): string {
  const configured = environment['STUDY_LEDGER_FILE'];
  return configured === undefined || configured.trim() === ''
    ? join(homedir(), '.studyledger.json')
    : configured;
}

export async function run(processLike: ProcessLike): Promise<number> {
  try {
    const command = parseCommand(processLike.argv.slice(2));
    const result = await executeCommand(command, {
      dataPath: dataPath(processLike.env),
      now: () => new Date(),
      load: loadLedger,
      save: saveLedger,
    });
    processLike.stdout.write(result.stdout);
    return result.exitCode;
  } catch (error: unknown) {
    processLike.stderr.write(renderError(error));
    if (error instanceof CommandError) processLike.stderr.write(renderHelp());
    return error instanceof CommandError ? 2 : error instanceof StudyLedgerError ? 1 : 1;
  }
}

const entry = process.argv[1];
if (entry !== undefined && import.meta.url === pathToFileURL(entry).href) {
  process.exitCode = await run(process);
}
