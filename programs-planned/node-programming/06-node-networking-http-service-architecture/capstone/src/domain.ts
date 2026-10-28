import { createHash } from 'node:crypto';
import { ServiceProblem } from './errors.js';

export type Operation = 'uppercase' | 'word-count' | 'checksum' | 'sleep';

export interface SubmitCommand {
  readonly operation: Operation;
  readonly payload: string;
}

export type JobId = string & { readonly __jobId: unique symbol };
export type IdempotencyKey = string & { readonly __idempotencyKey: unique symbol };

export type JobState =
  | { readonly kind: 'queued' }
  | { readonly kind: 'running'; readonly startedAtMs: number }
  | {
      readonly kind: 'succeeded';
      readonly startedAtMs: number;
      readonly completedAtMs: number;
      readonly result: string;
    }
  | {
      readonly kind: 'failed';
      readonly startedAtMs: number;
      readonly completedAtMs: number;
      readonly code: string;
      readonly message: string;
    }
  | {
      readonly kind: 'cancelled';
      readonly completedAtMs: number;
      readonly cause: 'shutdown' | 'user';
    };

export interface Job {
  readonly id: JobId;
  readonly operation: Operation;
  readonly payload: string;
  readonly createdAtMs: number;
  readonly revision: number;
  readonly state: JobState;
}

export interface JobView {
  readonly id: string;
  readonly operation: Operation;
  readonly revision: number;
  readonly state: JobState['kind'];
  readonly result?: string;
  readonly error?: { readonly code: string; readonly message: string };
}

const JOB_ID = /^job-\d{6}$/;
const IDEMPOTENCY_KEY = /^[A-Za-z0-9._:-]{8,128}$/;

export function parseJobId(value: string): JobId {
  if (!JOB_ID.test(value)) throw new ServiceProblem('INVALID_REQUEST', 422, 'Invalid job identifier');
  return value as JobId;
}

export function parseIdempotencyKey(value: string | undefined): IdempotencyKey {
  if (value === undefined) {
    throw new ServiceProblem('IDEMPOTENCY_KEY_REQUIRED', 400, 'Idempotency-Key is required');
  }
  if (!IDEMPOTENCY_KEY.test(value)) {
    throw new ServiceProblem('INVALID_REQUEST', 422, 'Idempotency-Key has invalid syntax');
  }
  return value as IdempotencyKey;
}

export function validateSubmitCommand(value: unknown, maxPayloadBytes = 16 * 1024): SubmitCommand {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new ServiceProblem('INVALID_REQUEST', 422, 'Submission must be a JSON object');
  }
  const record = value as Record<string, unknown>;
  const keys = Object.keys(record).sort().join(',');
  if (keys !== 'operation,payload') {
    throw new ServiceProblem('INVALID_REQUEST', 422, 'Submission must contain exactly operation and payload');
  }
  if (
    record.operation !== 'uppercase' &&
    record.operation !== 'word-count' &&
    record.operation !== 'checksum' &&
    record.operation !== 'sleep'
  ) {
    throw new ServiceProblem('INVALID_REQUEST', 422, 'Unsupported operation');
  }
  if (typeof record.payload !== 'string' || Buffer.byteLength(record.payload, 'utf8') > maxPayloadBytes) {
    throw new ServiceProblem('INVALID_REQUEST', 422, 'Payload is invalid or too large');
  }
  if (record.operation === 'sleep') {
    const duration = Number(record.payload);
    if (!Number.isSafeInteger(duration) || duration < 0) {
      throw new ServiceProblem('INVALID_REQUEST', 422, 'sleep payload must be non-negative integer milliseconds');
    }
  }
  return { operation: record.operation, payload: record.payload };
}

export function fingerprintCommand(command: SubmitCommand): string {
  return createHash('sha256')
    .update(command.operation)
    .update('\0')
    .update(command.payload)
    .digest('hex');
}

export function jobEtag(job: Pick<Job, 'id' | 'revision'>): string {
  return `"job-${job.id}-rev-${job.revision}"`;
}

export function toJobView(job: Job): JobView {
  switch (job.state.kind) {
    case 'queued':
    case 'running':
    case 'cancelled':
      return { id: job.id, operation: job.operation, revision: job.revision, state: job.state.kind };
    case 'succeeded':
      return {
        id: job.id,
        operation: job.operation,
        revision: job.revision,
        state: 'succeeded',
        result: job.state.result,
      };
    case 'failed':
      return {
        id: job.id,
        operation: job.operation,
        revision: job.revision,
        state: 'failed',
        error: { code: job.state.code, message: job.state.message },
      };
  }
}
