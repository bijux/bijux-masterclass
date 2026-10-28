import { createHash } from 'node:crypto';

export type Operation = 'uppercase' | 'word-count';
export interface SubmitCommand { readonly operation: Operation; readonly payload: string; }
export interface JobView {
  readonly id: string;
  readonly revision: number;
  readonly state: 'queued';
  readonly operation: Operation;
}
export type Route =
  | { readonly kind: 'health'; readonly head: boolean }
  | { readonly kind: 'submit' }
  | { readonly kind: 'job'; readonly id: string; readonly head: boolean }
  | { readonly kind: 'method-not-allowed'; readonly allow: string }
  | { readonly kind: 'not-found' };

export interface FiniteRequest {
  readonly method: string;
  readonly url: URL;
  readonly headers: ReadonlyMap<string, string>;
  readonly body?: unknown;
}
export interface FiniteResponse {
  readonly status: number;
  readonly headers: ReadonlyMap<string, string>;
  readonly body?: unknown;
}

const JOB_ID = /^job-\d{6}$/;
const IDEMPOTENCY_KEY = /^[A-Za-z0-9._:-]{8,128}$/;

export function matchRoute(method: string, url: URL): Route {
  const head = method === 'HEAD';
  if (url.pathname === '/health') {
    if (method === 'GET' || head) return { kind: 'health', head };
    return { kind: 'method-not-allowed', allow: 'GET, HEAD' };
  }
  if (url.pathname === '/jobs') {
    if (method === 'POST') return { kind: 'submit' };
    return { kind: 'method-not-allowed', allow: 'POST' };
  }
  const segments = url.pathname.split('/');
  if (segments.length === 3 && segments[1] === 'jobs' && segments[2] && JOB_ID.test(segments[2])) {
    if (method === 'GET' || head) return { kind: 'job', id: segments[2], head };
    return { kind: 'method-not-allowed', allow: 'GET, HEAD' };
  }
  return { kind: 'not-found' };
}

export function validateSubmission(value: unknown): SubmitCommand {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('submission must be an object');
  }
  const record = value as Record<string, unknown>;
  const keys = Object.keys(record).sort();
  if (keys.join(',') !== 'operation,payload') throw new Error('submission has unexpected fields');
  if (record.operation !== 'uppercase' && record.operation !== 'word-count') {
    throw new Error('unsupported operation');
  }
  if (typeof record.payload !== 'string' || Buffer.byteLength(record.payload, 'utf8') > 256) {
    throw new Error('invalid payload');
  }
  return { operation: record.operation, payload: record.payload };
}

function fingerprint(command: SubmitCommand): string {
  return createHash('sha256')
    .update(command.operation)
    .update('\0')
    .update(command.payload)
    .digest('hex');
}

function etag(job: JobView): string {
  return `"job-${job.id}-rev-${job.revision}"`;
}

export class Application {
  readonly #jobs = new Map<string, JobView>();
  readonly #idempotency = new Map<string, { readonly fingerprint: string; readonly job: JobView }>();
  #next = 1;

  constructor(readonly maxJobs: number, readonly maxIdempotency: number) {}

  submit(command: SubmitCommand, key: string): { readonly job: JobView; readonly replay: boolean } {
    if (!IDEMPOTENCY_KEY.test(key)) throw new Error('invalid idempotency key');
    const digest = fingerprint(command);
    const existing = this.#idempotency.get(key);
    if (existing) {
      if (existing.fingerprint !== digest) throw new Error('IDEMPOTENCY_CONFLICT');
      return { job: existing.job, replay: true };
    }
    if (this.#jobs.size >= this.maxJobs || this.#idempotency.size >= this.maxIdempotency) {
      throw new Error('OVER_CAPACITY');
    }
    const id = `job-${String(this.#next).padStart(6, '0')}`;
    this.#next += 1;
    const job: JobView = { id, revision: 1, state: 'queued', operation: command.operation };
    this.#jobs.set(id, job);
    this.#idempotency.set(key, { fingerprint: digest, job });
    return { job, replay: false };
  }

  get(id: string): JobView | undefined { return this.#jobs.get(id); }

  dispatch(request: FiniteRequest): FiniteResponse {
    const route = matchRoute(request.method, request.url);
    switch (route.kind) {
      case 'health':
        return { status: 200, headers: new Map([['content-type', 'application/json']]), body: route.head ? undefined : { ok: true } };
      case 'method-not-allowed':
        return { status: 405, headers: new Map([['allow', route.allow]]) };
      case 'not-found':
        return { status: 404, headers: new Map() };
      case 'submit': {
        const key = request.headers.get('idempotency-key');
        if (key === undefined) return { status: 400, headers: new Map(), body: { code: 'IDEMPOTENCY_KEY_REQUIRED' } };
        try {
          const result = this.submit(validateSubmission(request.body), key);
          return {
            status: 202,
            headers: new Map([['etag', etag(result.job)], ['location', `/jobs/${result.job.id}`]]),
            body: { ...result.job, replay: result.replay },
          };
        } catch (error) {
          const message = error instanceof Error ? error.message : 'INTERNAL';
          const status = message === 'IDEMPOTENCY_CONFLICT' ? 409 : message === 'OVER_CAPACITY' ? 503 : 422;
          return { status, headers: new Map(), body: { code: message } };
        }
      }
      case 'job': {
        const job = this.get(route.id);
        if (!job) return { status: 404, headers: new Map(), body: { code: 'JOB_NOT_FOUND' } };
        const tag = etag(job);
        if (request.headers.get('if-none-match') === tag) return { status: 304, headers: new Map([['etag', tag]]) };
        return { status: 200, headers: new Map([['etag', tag]]), body: route.head ? undefined : job };
      }
    }
  }
}
