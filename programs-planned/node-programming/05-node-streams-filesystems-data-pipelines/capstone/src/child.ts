import { spawn } from 'node:child_process';
import { createReadStream } from 'node:fs';
import { pipeline } from 'node:stream/promises';

import { asFlowError, FlowError } from './errors.js';
import { DEFAULT_LIMITS, type FlowLimits } from './limits.js';
import { ByteLimit, ByteTap } from './streams.js';
import { withTransactionalOutput } from './transaction.js';

async function collectBounded(
  source: NodeJS.ReadableStream,
  limit: number,
): Promise<{
  readonly text: string;
  readonly bytes: number;
  readonly truncated: boolean;
}> {
  const parts: Buffer[] = [];
  let total = 0;
  let kept = 0;

  for await (const raw of source) {
    const chunk = Buffer.from(raw);
    total += chunk.length;
    if (kept < limit) {
      const visible = chunk.subarray(0, limit - kept);
      parts.push(Buffer.from(visible));
      kept += visible.length;
    }
  }

  return {
    text: Buffer.concat(parts).toString('utf8'),
    bytes: total,
    truncated: total > limit,
  };
}

function waitForSpawn(child: ReturnType<typeof spawn>): Promise<void> {
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

function waitForClose(
  child: ReturnType<typeof spawn>,
): Promise<readonly [number | null, NodeJS.Signals | null]> {
  return new Promise((resolve) => {
    child.once('close', (code, signal) => resolve([code, signal] as const));
  });
}

function rejectedReason(
  state: PromiseSettledResult<unknown>,
): unknown | undefined {
  return state.status === 'rejected' ? state.reason : undefined;
}

function validateChildCommand(program: string, args: readonly string[]): void {
  if (program.length === 0) {
    throw new FlowError('CHILD_FAILED', 'child program is required');
  }
  if (program.includes('\0') || args.some((argument) => argument.includes('\0'))) {
    throw new FlowError('CHILD_FAILED', 'child program and arguments cannot contain NUL');
  }
}

export interface ChildReport {
  readonly operation: 'through';
  readonly inputBytes: number;
  readonly inputSha256: string;
  readonly outputBytes: number;
  readonly outputSha256: string;
  readonly stderrBytes: number;
  readonly stderrTruncated: boolean;
  readonly committed: true;
}

export async function throughChild(
  input: string,
  output: string,
  program: string,
  args: readonly string[],
  replace: boolean,
  signal?: AbortSignal,
  limits: FlowLimits = DEFAULT_LIMITS,
): Promise<ChildReport> {
  validateChildCommand(program, args);
  signal?.throwIfAborted();

  return withTransactionalOutput(output, { replace }, async (sink) => {
    const child = spawn(program, [...args], {
      shell: false,
      stdio: ['pipe', 'pipe', 'pipe'],
      signal,
      windowsHide: true,
    });
    const closePromise = waitForClose(child);
    let processError: Error | undefined;
    child.on('error', (error) => {
      processError ??= error;
    });

    try {
      await waitForSpawn(child);
    } catch (error) {
      if (child.pid !== undefined && !child.killed) {
        child.kill();
      }
      await closePromise;
      throw asFlowError(
        processError ?? error,
        'CHILD_FAILED',
        `failed to spawn ${program}`,
      );
    }

    if (!child.stdin || !child.stdout || !child.stderr) {
      if (!child.killed) {
        child.kill();
      }
      await closePromise;
      throw new FlowError('CHILD_FAILED', 'child stdio pipes unavailable');
    }

    const sourceLimit = new ByteLimit(
      limits.maxSourceBytes,
      'SOURCE_LIMIT',
      'source',
    );
    const inputTap = new ByteTap(true);
    const childOutputLimit = new ByteLimit(
      limits.maxChildOutputBytes,
      'CHILD_OUTPUT_LIMIT',
      'child output',
    );
    const outputTap = new ByteTap(true);

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

    const inputFlow = terminateOnFailure(
      pipeline(
        createReadStream(input),
        sourceLimit,
        inputTap,
        child.stdin,
        { signal },
      ),
    );
    const outputFlow = terminateOnFailure(
      pipeline(
        child.stdout,
        childOutputLimit,
        outputTap,
        sink,
        { signal },
      ),
    );
    const stderrFlow = terminateOnFailure(
      collectBounded(child.stderr, limits.maxChildStderrBytes),
    );

    const states = await Promise.allSettled([
      inputFlow,
      outputFlow,
      stderrFlow,
      closePromise,
    ]);

    if (signal?.aborted) {
      throw asFlowError(
        signal.reason,
        'CHILD_FAILED',
        'child operation cancelled',
      );
    }

    const outputError = rejectedReason(states[1]);
    if (outputError !== undefined) {
      throw asFlowError(outputError, 'CHILD_FAILED', 'child stdout pipeline failed');
    }
    const stderrError = rejectedReason(states[2]);
    if (stderrError !== undefined) {
      throw asFlowError(stderrError, 'CHILD_FAILED', 'child stderr pipeline failed');
    }

    const [code, terminationSignal] = (
      states[3] as PromiseFulfilledResult<
        readonly [number | null, NodeJS.Signals | null]
      >
    ).value;
    const diagnostics = (
      states[2] as PromiseFulfilledResult<{
        readonly text: string;
        readonly bytes: number;
        readonly truncated: boolean;
      }>
    ).value;

    if (terminationSignal !== null) {
      throw new FlowError(
        'CHILD_FAILED',
        `child terminated by signal ${terminationSignal}`,
      );
    }
    if (code !== 0) {
      throw new FlowError(
        'CHILD_FAILED',
        `child exited with code ${String(code)}; stderr=${diagnostics.text}`,
      );
    }

    const inputError = rejectedReason(states[0]);
    if (inputError !== undefined) {
      throw asFlowError(inputError, 'CHILD_FAILED', 'child stdin pipeline failed');
    }
    if (processError) {
      throw asFlowError(processError, 'CHILD_FAILED', 'child process failed');
    }

    return {
      operation: 'through',
      inputBytes: inputTap.bytes,
      inputSha256: inputTap.digestHex(),
      outputBytes: outputTap.bytes,
      outputSha256: outputTap.digestHex(),
      stderrBytes: diagnostics.bytes,
      stderrTruncated: diagnostics.truncated,
      committed: true,
    };
  });
}
