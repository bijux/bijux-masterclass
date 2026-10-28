import { randomUUID } from 'node:crypto';
import { mkdir, readFile, rename, rm, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { decodeLedger, encodeLedger } from './codec.js';
import { emptyLedger, type StudyLedger } from './domain.js';
import { StorageIoError, StorageValidationError } from './errors.js';

export const MAX_STORAGE_BYTES = 5_000_000;

function isNodeError(error: unknown): error is NodeJS.ErrnoException {
  return error instanceof Error && 'code' in error;
}

export async function loadLedger(path: string): Promise<StudyLedger> {
  let text: string;
  try {
    text = await readFile(path, 'utf8');
  } catch (error: unknown) {
    if (isNodeError(error) && error.code === 'ENOENT') return emptyLedger();
    throw new StorageIoError('read', path, { cause: error });
  }
  if (Buffer.byteLength(text, 'utf8') > MAX_STORAGE_BYTES) {
    throw new StorageValidationError([
      { path: '$', message: `ledger exceeds the ${MAX_STORAGE_BYTES}-byte course limit` },
    ]);
  }
  return decodeLedger(text);
}

export async function saveLedger(path: string, ledger: StudyLedger): Promise<void> {
  const directory = dirname(path);
  const temporary = join(directory, `.${randomUUID()}.studyledger.tmp`);
  try {
    await mkdir(directory, { recursive: true });
    await writeFile(temporary, encodeLedger(ledger), { encoding: 'utf8', flag: 'wx' });
    await rename(temporary, path);
  } catch (error: unknown) {
    try {
      await rm(temporary, { force: true });
    } catch {
      // The original write or replace failure remains the causal error.
    }
    throw new StorageIoError('save', path, { cause: error });
  }
}
