import { randomUUID } from 'node:crypto';
import { createWriteStream } from 'node:fs';
import { open, rename, rm, stat } from 'node:fs/promises';
import { basename, dirname, join } from 'node:path';
import type { Writable } from 'node:stream';

import { asFlowError, FlowError } from './errors.js';

export interface TransactionOptions {
  readonly replace: boolean;
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

export async function withTransactionalOutput<T>(
  destination: string,
  options: TransactionOptions,
  operation: (sink: Writable) => Promise<T>,
): Promise<T> {
  const stage = join(
    dirname(destination),
    `.${basename(destination)}.${randomUUID()}.tmp`,
  );
  let committed = false;

  try {
    const sink = createWriteStream(stage, { flags: 'wx', mode: 0o600 });
    const result = await operation(sink);

    const handle = await open(stage, 'r+');
    try {
      await handle.sync();
    } finally {
      await handle.close();
    }

    if (!options.replace && (await destinationExists(destination))) {
      throw new FlowError('COMMIT', 'destination already exists');
    }

    await rename(stage, destination);
    committed = true;
    return result;
  } catch (error) {
    throw asFlowError(error, 'COMMIT', `failed to publish ${destination}`);
  } finally {
    if (!committed) {
      await rm(stage, { force: true }).catch(() => undefined);
    }
  }
}
