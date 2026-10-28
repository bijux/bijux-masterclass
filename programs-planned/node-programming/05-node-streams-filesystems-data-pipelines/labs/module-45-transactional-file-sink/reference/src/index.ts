import { randomUUID } from 'node:crypto';
import { createReadStream, createWriteStream } from 'node:fs';
import { open, rename, rm, stat } from 'node:fs/promises';
import { basename, dirname, join } from 'node:path';
import { pipeline } from 'node:stream/promises';

export interface TransactionOptions {
  readonly replace?: boolean;
  readonly mode?: number;
  readonly signal?: AbortSignal;
}

export interface TransactionReport {
  readonly bytes: number;
  readonly committed: true;
}

async function destinationExists(path: string): Promise<boolean> {
  try {
    await stat(path);
    return true;
  } catch (error) {
    if (
      error instanceof Error &&
      'code' in error &&
      (error as NodeJS.ErrnoException).code === 'ENOENT'
    ) {
      return false;
    }
    throw error;
  }
}

export async function transactionalWrite(
  destination: string,
  source: AsyncIterable<Uint8Array>,
  options: TransactionOptions = {},
): Promise<TransactionReport> {
  options.signal?.throwIfAborted();

  const stage = join(
    dirname(destination),
    `.${basename(destination)}.${randomUUID()}.tmp`,
  );
  let committed = false;
  let bytes = 0;

  try {
    async function* counted(): AsyncGenerator<Uint8Array> {
      for await (const chunk of source) {
        options.signal?.throwIfAborted();
        bytes += chunk.byteLength;
        yield chunk;
      }
    }

    const stream = createWriteStream(stage, {
      flags: 'wx',
      mode: options.mode ?? 0o600,
    });
    await pipeline(counted(), stream, { signal: options.signal });

    const handle = await open(stage, 'r+');
    try {
      await handle.sync();
    } finally {
      await handle.close();
    }

    if (!options.replace && (await destinationExists(destination))) {
      throw new Error('destination already exists');
    }

    await rename(stage, destination);
    committed = true;
    return { bytes, committed: true };
  } finally {
    if (!committed) {
      await rm(stage, { force: true }).catch(() => undefined);
    }
  }
}

export async function copyTransactional(
  source: string,
  destination: string,
  options: TransactionOptions = {},
): Promise<TransactionReport> {
  return transactionalWrite(destination, createReadStream(source), options);
}
