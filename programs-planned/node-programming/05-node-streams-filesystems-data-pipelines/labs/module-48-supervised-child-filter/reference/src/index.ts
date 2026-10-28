import { spawn, type ChildProcessWithoutNullStreams } from 'node:child_process';
import { Readable } from 'node:stream';
import { pipeline } from 'node:stream/promises';

export interface ChildCommand {
  readonly program: string;
  readonly args: readonly string[];
}

export interface ChildFilterOptions extends ChildCommand {
  readonly input: Uint8Array;
  readonly maxStdoutBytes: number;
  readonly stderrLimit: number;
  readonly signal?: AbortSignal;
}

export interface ChildFilterResult {
  readonly stdout: Buffer;
  readonly stderr: Buffer;
  readonly stderrTruncated: boolean;
  readonly code: 0;
}

export class ChildOutputLimitError extends Error {
  constructor(readonly limit: number) {
    super(`child stdout exceeds ${limit} bytes`);
    this.name = 'ChildOutputLimitError';
  }
}

export function validateCommand(command: ChildCommand): void {
  if (command.program.length === 0) {
    throw new Error('program is required');
  }
  if (command.program.includes('\0')) {
    throw new Error('program cannot contain NUL');
  }
  if (command.args.some((argument) => argument.includes('\0'))) {
    throw new Error('arguments cannot contain NUL');
  }
}

function validateLimit(value: number, name: string): void {
  if (!Number.isInteger(value) || value < 0) {
    throw new RangeError(`${name} must be a non-negative integer`);
  }
}

async function collectRetained(
  source: NodeJS.ReadableStream,
  limit: number,
): Promise<{ readonly buffer: Buffer; readonly truncated: boolean }> {
  const parts: Buffer[] = [];
  let kept = 0;
  let total = 0;

  for await (const raw of source) {
    const chunk = Buffer.from(raw);
    total += chunk.length;
    if (kept < limit) {
      const visible = chunk.subarray(0, limit - kept);
      parts.push(Buffer.from(visible));
      kept += visible.length;
    }
  }

  return { buffer: Buffer.concat(parts), truncated: total > limit };
}

async function collectStrict(
  source: NodeJS.ReadableStream,
  limit: number,
): Promise<Buffer> {
  const parts: Buffer[] = [];
  let total = 0;

  for await (const raw of source) {
    const chunk = Buffer.from(raw);
    total += chunk.length;
    if (total > limit) {
      throw new ChildOutputLimitError(limit);
    }
    parts.push(Buffer.from(chunk));
  }

  return Buffer.concat(parts);
}

function reaped(
  child: ChildProcessWithoutNullStreams,
): Promise<readonly [number | null, NodeJS.Signals | null]> {
  return new Promise((resolve) => {
    child.once('close', (code, signal) => resolve([code, signal] as const));
  });
}

function spawned(child: ChildProcessWithoutNullStreams): Promise<void> {
  return new Promise((resolve, reject) => {
    const onSpawn = (): void => {
      child.off('error', onError);
      resolve();
    };
    const onError = (error: Error): void => {
      child.off('spawn', onSpawn);
      reject(error);
    };
    child.once('spawn', onSpawn);
    child.once('error', onError);
  });
}

function firstRejected(
  states: readonly PromiseSettledResult<unknown>[],
): unknown | undefined {
  return states.find(
    (state): state is PromiseRejectedResult => state.status === 'rejected',
  )?.reason;
}

export async function runChildFilter(
  options: ChildFilterOptions,
): Promise<ChildFilterResult> {
  validateCommand(options);
  validateLimit(options.maxStdoutBytes, 'maxStdoutBytes');
  validateLimit(options.stderrLimit, 'stderrLimit');
  options.signal?.throwIfAborted();

  const child = spawn(options.program, [...options.args], {
    shell: false,
    stdio: ['pipe', 'pipe', 'pipe'],
    signal: options.signal,
    windowsHide: true,
  });
  const closePromise = reaped(child);
  let processError: Error | undefined;
  child.on('error', (error) => {
    processError ??= error;
  });

  try {
    await spawned(child);
  } catch (error) {
    if (child.pid !== undefined && !child.killed) {
      child.kill();
    }
    await closePromise;
    throw processError ?? error;
  }

  const terminateOnFailure = async <T>(promise: Promise<T>): Promise<T> => {
    try {
      return await promise;
    } catch (error) {
      if (!child.killed) {
        child.kill();
      }
      throw error;
    }
  };

  const inputPromise = terminateOnFailure(
    pipeline(Readable.from([Buffer.from(options.input)]), child.stdin),
  );
  const stdoutPromise = terminateOnFailure(
    collectStrict(child.stdout, options.maxStdoutBytes),
  );
  const stderrPromise = terminateOnFailure(
    collectRetained(child.stderr, options.stderrLimit),
  );

  const states = await Promise.allSettled([
    inputPromise,
    stdoutPromise,
    stderrPromise,
    closePromise,
  ]);
  const rejected = firstRejected(states);
  if (rejected !== undefined) {
    throw rejected;
  }
  if (processError) {
    throw processError;
  }

  const stdout = (states[1] as PromiseFulfilledResult<Buffer>).value;
  const stderr = (
    states[2] as PromiseFulfilledResult<{
      readonly buffer: Buffer;
      readonly truncated: boolean;
    }>
  ).value;
  const [code, signal] = (
    states[3] as PromiseFulfilledResult<
      readonly [number | null, NodeJS.Signals | null]
    >
  ).value;

  if (signal !== null) {
    throw new Error(`child terminated by signal ${signal}`);
  }
  if (code !== 0) {
    throw new Error(
      `child exited with code ${String(code)}; stderr=${stderr.buffer.toString('utf8')}`,
    );
  }

  return {
    stdout,
    stderr: stderr.buffer,
    stderrTruncated: stderr.truncated,
    code: 0,
  };
}
