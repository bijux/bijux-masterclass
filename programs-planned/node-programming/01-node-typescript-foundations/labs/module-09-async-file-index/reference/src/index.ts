import { readdir, stat } from 'node:fs/promises';
import { join } from 'node:path';

export interface FileEntry { readonly name: string; readonly size: number; readonly modifiedAtMs: number }

function throwIfAborted(signal: AbortSignal | undefined): void {
  if (signal?.aborted === true) throw signal.reason ?? new Error('operation aborted');
}

export async function indexDirectory(directory: string, maxEntries: number, signal?: AbortSignal): Promise<FileEntry[]> {
  if (!Number.isSafeInteger(maxEntries) || maxEntries < 0) throw new Error('maxEntries must be a nonnegative safe integer');
  throwIfAborted(signal);
  const names = await readdir(directory);
  if (names.length > maxEntries) throw new Error(`directory contains ${names.length} entries; maximum is ${maxEntries}`);
  const candidates = await Promise.all(names.map(async (name): Promise<FileEntry | undefined> => {
    throwIfAborted(signal);
    const path = join(directory, name);
    try {
      const information = await stat(path);
      return information.isFile() ? { name, size: information.size, modifiedAtMs: information.mtimeMs } : undefined;
    } catch (error: unknown) {
      throw new Error(`cannot inspect ${path}`, { cause: error });
    }
  }));
  return candidates.filter((entry): entry is FileEntry => entry !== undefined)
    .sort((left, right) => left.name.localeCompare(right.name, 'en'));
}

export function renderEntries(entries: readonly FileEntry[]): string {
  return entries.map((entry) => `${entry.name}\t${entry.size}\t${entry.modifiedAtMs}`).join('\n') + (entries.length === 0 ? '' : '\n');
}
