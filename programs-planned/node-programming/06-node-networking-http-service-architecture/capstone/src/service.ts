import { createHash } from 'node:crypto';
import { setTimeout as delay } from 'node:timers/promises';
import type { ServiceLimits } from './config.js';
import {
  fingerprintCommand,
  jobEtag,
  toJobView,
  type IdempotencyKey,
  type Job,
  type JobId,
  type JobView,
  type SubmitCommand,
} from './domain.js';
import { EventJournal } from './events.js';
import { ServiceProblem } from './errors.js';

interface IdempotencyRecord {
  readonly fingerprint: string;
  readonly jobId: JobId;
  readonly createdAtMs: number;
}

export interface SubmissionResult {
  readonly job: JobView;
  readonly etag: string;
  readonly replay: boolean;
}

export interface ServiceStats {
  readonly health: 'healthy';
  readonly readiness: 'ready' | 'not-ready';
  readonly state: 'ready' | 'quiescing' | 'stopped';
  readonly queued: number;
  readonly active: number;
  readonly retainedJobs: number;
  readonly idempotencyRecords: number;
  readonly eventSequence: number;
  readonly subscribers: number;
}

export interface ServiceTerminalReport {
  readonly acceptedJobs: number;
  readonly succeededJobs: number;
  readonly failedJobs: number;
  readonly cancelledJobs: number;
  readonly remainingTasks: number;
  readonly remainingSubscribers: number;
}

export class ServiceWireApplication {
  readonly #jobs = new Map<JobId, Job>();
  readonly #idempotency = new Map<IdempotencyKey, IdempotencyRecord>();
  readonly #queue: JobId[] = [];
  readonly #tasks = new Set<Promise<void>>();
  readonly #controllers = new Map<JobId, AbortController>();
  #nextId = 1;
  #active = 0;
  #state: 'ready' | 'quiescing' | 'stopped' = 'ready';
  #closePromise: Promise<ServiceTerminalReport> | undefined;

  constructor(
    readonly limits: ServiceLimits,
    readonly events = new EventJournal(limits.maxEvents, limits.maxSubscribers),
    readonly now: () => number = Date.now,
  ) {}

  submit(command: SubmitCommand, key: IdempotencyKey): SubmissionResult {
    if (this.#state !== 'ready') {
      throw new ServiceProblem('NOT_READY', 503, 'Service is not accepting new jobs');
    }
    const fingerprint = fingerprintCommand(command);
    const existing = this.#idempotency.get(key);
    if (existing) {
      if (existing.fingerprint !== fingerprint) {
        throw new ServiceProblem('IDEMPOTENCY_CONFLICT', 409, 'Idempotency key was used for a different request');
      }
      const job = this.requireJob(existing.jobId);
      return { job: toJobView(job), etag: jobEtag(job), replay: true };
    }
    if (this.#jobs.size >= this.limits.maxJobs || this.#idempotency.size >= this.limits.maxIdempotencyRecords) {
      throw new ServiceProblem('OVER_CAPACITY', 503, 'Job or idempotency capacity is full');
    }
    if (this.#nextId > 999_999) {
      throw new ServiceProblem('OVER_CAPACITY', 503, 'Job identifier space is exhausted');
    }

    const id = `job-${String(this.#nextId).padStart(6, '0')}` as JobId;
    this.#nextId += 1;
    const createdAtMs = this.now();
    const job: Job = {
      id,
      operation: command.operation,
      payload: command.payload,
      createdAtMs,
      revision: 1,
      state: { kind: 'queued' },
    };
    this.#idempotency.set(key, { fingerprint, jobId: id, createdAtMs });
    this.#jobs.set(id, job);
    this.#queue.push(id);
    this.events.append({
      type: 'job-created',
      occurredAtMs: createdAtMs,
      jobId: id,
      revision: 1,
    });
    queueMicrotask(() => this.pump());
    return { job: toJobView(job), etag: jobEtag(job), replay: false };
  }

  getJob(id: JobId): { readonly job: JobView; readonly etag: string } | undefined {
    const job = this.#jobs.get(id);
    return job ? { job: toJobView(job), etag: jobEtag(job) } : undefined;
  }

  stats(): ServiceStats {
    let queued = 0;
    for (const job of this.#jobs.values()) if (job.state.kind === 'queued') queued += 1;
    return {
      health: 'healthy',
      readiness: this.#state === 'ready' ? 'ready' : 'not-ready',
      state: this.#state,
      queued,
      active: this.#active,
      retainedJobs: this.#jobs.size,
      idempotencyRecords: this.#idempotency.size,
      eventSequence: this.events.latestSequence(),
      subscribers: this.events.subscriberCount(),
    };
  }

  quiesce(): void {
    if (this.#state !== 'ready') return;
    this.#state = 'quiescing';
    this.events.append({ type: 'service-quiescing', occurredAtMs: this.now() });
  }

  async waitForIdle(budgetMs: number): Promise<boolean> {
    const deadline = Date.now() + budgetMs;
    while ((this.#queue.length > 0 || this.#tasks.size > 0 || this.#active > 0) && Date.now() < deadline) {
      await delay(2);
    }
    return this.#queue.length === 0 && this.#tasks.size === 0 && this.#active === 0;
  }

  close(graceMs = this.limits.shutdownGraceMs): Promise<ServiceTerminalReport> {
    if (this.#closePromise) return this.#closePromise;
    this.#closePromise = this.closeOwned(graceMs);
    return this.#closePromise;
  }

  private async closeOwned(graceMs: number): Promise<ServiceTerminalReport> {
    this.quiesce();
    const drained = await this.waitForIdle(graceMs);
    if (!drained) {
      for (const id of this.#queue.splice(0)) this.cancelQueued(id);
      for (const controller of this.#controllers.values()) controller.abort(new Error('service shutdown'));
      await Promise.allSettled([...this.#tasks]);
      for (const job of this.#jobs.values()) {
        if (job.state.kind === 'running' || job.state.kind === 'queued') {
          this.transitionCancelled(job.id, 'shutdown');
        }
      }
    }
    this.events.close();
    this.#state = 'stopped';
    const jobs = [...this.#jobs.values()];
    return {
      acceptedJobs: jobs.length,
      succeededJobs: jobs.filter((job) => job.state.kind === 'succeeded').length,
      failedJobs: jobs.filter((job) => job.state.kind === 'failed').length,
      cancelledJobs: jobs.filter((job) => job.state.kind === 'cancelled').length,
      remainingTasks: this.#tasks.size,
      remainingSubscribers: this.events.subscriberCount(),
    };
  }

  private pump(): void {
    if (this.#state === 'stopped') return;
    while (this.#active < this.limits.maxActiveJobs) {
      const id = this.#queue.shift();
      if (id === undefined) break;
      const job = this.#jobs.get(id);
      if (!job || job.state.kind !== 'queued') continue;
      this.#active += 1;
      const controller = new AbortController();
      this.#controllers.set(id, controller);
      this.transitionRunning(id);
      const task = this.execute(id, controller.signal)
        .catch((error: unknown) => {
          const current = this.#jobs.get(id);
          if (current?.state.kind !== 'running') return;
          if (controller.signal.aborted) {
            this.transitionCancelled(id, 'shutdown');
          } else {
            this.transitionFailed(id, error);
          }
        })
        .finally(() => {
          this.#active -= 1;
          this.#controllers.delete(id);
          this.#tasks.delete(task);
          this.pump();
        });
      this.#tasks.add(task);
    }
  }

  private async execute(id: JobId, signal: AbortSignal): Promise<void> {
    const job = this.requireJob(id);
    let result: string;
    switch (job.operation) {
      case 'uppercase':
        result = job.payload.toUpperCase();
        break;
      case 'word-count': {
        const trimmed = job.payload.trim();
        result = String(trimmed === '' ? 0 : trimmed.split(/\s+/u).length);
        break;
      }
      case 'checksum':
        result = createHash('sha256').update(job.payload).digest('hex');
        break;
      case 'sleep': {
        const duration = Number(job.payload);
        if (!Number.isSafeInteger(duration) || duration < 0 || duration > this.limits.maxOperationMs) {
          throw new Error('sleep duration exceeds operation policy');
        }
        await delay(duration, undefined, { signal });
        result = `slept:${duration}`;
        break;
      }
    }
    const current = this.#jobs.get(id);
    if (current?.state.kind === 'running') this.transitionSucceeded(id, result);
  }

  private transitionRunning(id: JobId): void {
    const job = this.requireJob(id);
    if (job.state.kind !== 'queued') throw new Error('job is not queued');
    const startedAtMs = this.now();
    const next: Job = { ...job, revision: job.revision + 1, state: { kind: 'running', startedAtMs } };
    this.#jobs.set(id, next);
    this.events.append({ type: 'job-running', occurredAtMs: startedAtMs, jobId: id, revision: next.revision });
  }

  private transitionSucceeded(id: JobId, result: string): void {
    const job = this.requireJob(id);
    if (job.state.kind !== 'running') return;
    const completedAtMs = this.now();
    const next: Job = {
      ...job,
      revision: job.revision + 1,
      state: {
        kind: 'succeeded',
        startedAtMs: job.state.startedAtMs,
        completedAtMs,
        result: result.slice(0, this.limits.maxResponseBodyBytes),
      },
    };
    this.#jobs.set(id, next);
    this.events.append({ type: 'job-succeeded', occurredAtMs: completedAtMs, jobId: id, revision: next.revision });
  }

  private transitionFailed(id: JobId, error: unknown): void {
    const job = this.requireJob(id);
    if (job.state.kind !== 'running') return;
    const completedAtMs = this.now();
    const message = error instanceof Error ? error.message.slice(0, 160) : 'unknown operation failure';
    const next: Job = {
      ...job,
      revision: job.revision + 1,
      state: {
        kind: 'failed',
        startedAtMs: job.state.startedAtMs,
        completedAtMs,
        code: 'OPERATION_FAILED',
        message,
      },
    };
    this.#jobs.set(id, next);
    this.events.append({ type: 'job-failed', occurredAtMs: completedAtMs, jobId: id, revision: next.revision });
  }

  private cancelQueued(id: JobId): void {
    const job = this.#jobs.get(id);
    if (job?.state.kind === 'queued') this.transitionCancelled(id, 'shutdown');
  }

  private transitionCancelled(id: JobId, cause: 'shutdown' | 'user'): void {
    const job = this.#jobs.get(id);
    if (!job || !['queued', 'running'].includes(job.state.kind)) return;
    const completedAtMs = this.now();
    const next: Job = {
      ...job,
      revision: job.revision + 1,
      state: { kind: 'cancelled', completedAtMs, cause },
    };
    this.#jobs.set(id, next);
    this.events.append({ type: 'job-cancelled', occurredAtMs: completedAtMs, jobId: id, revision: next.revision });
  }

  private requireJob(id: JobId): Job {
    const job = this.#jobs.get(id);
    if (!job) throw new ServiceProblem('JOB_NOT_FOUND', 404, 'Job does not exist');
    return job;
  }
}
