import http from 'node:http';
import https from 'node:https';
import { performance } from 'node:perf_hooks';
import type { JobView, SubmitCommand } from './domain.js';
import type { Problem } from './errors.js';
import type { ServiceStats, SubmissionResult } from './service.js';

export interface ClientAttempt {
  readonly number: number;
  readonly outcome: 'response' | 'transport-error' | 'deadline';
  readonly status?: number;
  readonly code?: string;
}

export class ServiceWireClientError extends Error {
  constructor(
    readonly kind: 'deadline' | 'transport' | 'response-too-large' | 'protocol' | 'http' | 'closed',
    message: string,
    readonly attempts: readonly ClientAttempt[],
    readonly problem?: Problem,
  ) {
    super(message);
    this.name = 'ServiceWireClientError';
  }
}

interface RawResponse {
  readonly status: number;
  readonly headers: http.IncomingHttpHeaders;
  readonly body: Buffer;
}

export class ServiceWireClient {
  readonly #httpAgent: http.Agent;
  readonly #httpsAgent: https.Agent;
  #closed = false;

  constructor(readonly options: {
    readonly baseUrl: URL;
    readonly maxSockets: number;
    readonly maxResponseBytes: number;
    readonly maxAttempts: number;
    readonly ca?: Buffer;
    readonly servername?: string;
  }) {
    this.#httpAgent = new http.Agent({
      keepAlive: true,
      maxSockets: options.maxSockets,
      maxFreeSockets: options.maxSockets,
    });
    this.#httpsAgent = new https.Agent({
      keepAlive: true,
      maxSockets: options.maxSockets,
      maxFreeSockets: options.maxSockets,
      ...(options.ca ? { ca: options.ca } : {}),
    });
  }

  async submit(
    command: SubmitCommand,
    idempotencyKey: string,
    budgetMs = 1_000,
  ): Promise<SubmissionResult> {
    const body = Buffer.from(JSON.stringify(command), 'utf8');
    const response = await this.request({
      method: 'POST',
      path: '/v1/jobs',
      headers: {
        'content-type': 'application/json',
        'content-length': String(body.byteLength),
        'idempotency-key': idempotencyKey,
      },
      body,
      budgetMs,
      retry: true,
    });
    const value = this.parseJson(response) as {
      readonly id: string;
      readonly operation: JobView['operation'];
      readonly revision: number;
      readonly state: JobView['state'];
      readonly replay: boolean;
    };
    const etag = response.headers.etag;
    if (typeof value.id !== 'string' || typeof etag !== 'string') {
      throw new ServiceWireClientError('protocol', 'invalid submission response', []);
    }
    return {
      job: {
        id: value.id,
        operation: value.operation,
        revision: value.revision,
        state: value.state,
      },
      etag,
      replay: value.replay,
    };
  }

  async getJob(
    id: string,
    options: { readonly etag?: string; readonly budgetMs?: number } = {},
  ): Promise<{ readonly notModified: true; readonly etag: string } | {
    readonly notModified: false;
    readonly job: JobView;
    readonly etag: string;
  }> {
    const response = await this.request({
      method: 'GET',
      path: `/v1/jobs/${encodeURIComponent(id)}`,
      headers: options.etag ? { 'if-none-match': options.etag } : {},
      budgetMs: options.budgetMs ?? 1_000,
      retry: true,
    });
    const tag = response.headers.etag;
    if (typeof tag !== 'string') throw new ServiceWireClientError('protocol', 'missing ETag', []);
    if (response.status === 304) return { notModified: true, etag: tag };
    return { notModified: false, job: this.parseJson(response) as JobView, etag: tag };
  }

  async stats(budgetMs = 1_000): Promise<ServiceStats> {
    return this.parseJson(await this.request({
      method: 'GET',
      path: '/v1/stats',
      headers: {},
      budgetMs,
      retry: true,
    })) as ServiceStats;
  }

  async health(budgetMs = 1_000): Promise<{
    readonly health: 'healthy';
    readonly readiness: 'ready' | 'not-ready';
    readonly state: string;
  }> {
    return this.parseJson(await this.request({
      method: 'GET',
      path: '/v1/health',
      headers: {},
      budgetMs,
      retry: true,
    })) as {
      readonly health: 'healthy';
      readonly readiness: 'ready' | 'not-ready';
      readonly state: string;
    };
  }

  async waitForTerminal(id: string, budgetMs = 1_000): Promise<JobView> {
    const deadline = performance.now() + budgetMs;
    while (performance.now() < deadline) {
      const found = await this.getJob(id, { budgetMs: Math.max(1, deadline - performance.now()) });
      if (!found.notModified && ['succeeded', 'failed', 'cancelled'].includes(found.job.state)) return found.job;
      await new Promise((resolve) => setTimeout(resolve, 5));
    }
    throw new ServiceWireClientError('deadline', 'job did not become terminal before deadline', []);
  }

  private parseJson(response: RawResponse): unknown {
    const media = response.headers['content-type']?.split(';', 1)[0]?.toLowerCase();
    if (media !== 'application/json' && media !== 'application/problem+json') {
      throw new ServiceWireClientError('protocol', 'unexpected response media type', []);
    }
    try {
      return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(response.body)) as unknown;
    } catch {
      throw new ServiceWireClientError('protocol', 'response is not valid JSON', []);
    }
  }

  private async request(spec: {
    readonly method: string;
    readonly path: string;
    readonly headers: Readonly<Record<string, string>>;
    readonly body?: Buffer;
    readonly budgetMs: number;
    readonly retry: boolean;
  }): Promise<RawResponse> {
    if (this.#closed) throw new ServiceWireClientError('closed', 'client is closed', []);
    const deadline = performance.now() + spec.budgetMs;
    const attempts: ClientAttempt[] = [];
    for (let attempt = 1; attempt <= this.options.maxAttempts; attempt += 1) {
      const remaining = deadline - performance.now();
      if (remaining <= 0) throw new ServiceWireClientError('deadline', 'operation deadline expired', attempts);
      try {
        const response = await this.attempt(spec, remaining);
        attempts.push({ number: attempt, outcome: 'response', status: response.status });
        if (response.status >= 200 && response.status < 300 || response.status === 304) return response;
        let problem: Problem | undefined;
        try {
          problem = this.parseJson(response) as Problem;
        } catch {
          // Preserve HTTP status even when the error representation is malformed.
        }
        const retryable = spec.retry && response.status === 503 && attempt < this.options.maxAttempts;
        if (!retryable) {
          throw new ServiceWireClientError('http', `HTTP ${response.status}`, attempts, problem);
        }
      } catch (error) {
        if (error instanceof ServiceWireClientError) {
          if (error.kind === 'http' || error.kind === 'response-too-large' || error.kind === 'protocol') throw error;
          if (!spec.retry || attempt >= this.options.maxAttempts) throw error;
        } else {
          const maybeCode = error instanceof Error ? (error as NodeJS.ErrnoException).code : undefined;
          const code = typeof maybeCode === 'string' ? maybeCode : 'ERROR';
          attempts.push({ number: attempt, outcome: 'transport-error', code });
          if (!spec.retry || attempt >= this.options.maxAttempts) {
            throw new ServiceWireClientError('transport', 'request failed', attempts);
          }
        }
      }
      const waitMs = Math.min(20 * attempt, Math.max(0, deadline - performance.now()));
      if (waitMs <= 0) break;
      await new Promise((resolve) => setTimeout(resolve, waitMs));
    }
    throw new ServiceWireClientError('deadline', 'operation attempts exhausted', attempts);
  }

  private async attempt(
    spec: {
      readonly method: string;
      readonly path: string;
      readonly headers: Readonly<Record<string, string>>;
      readonly body?: Buffer;
    },
    remainingMs: number,
  ): Promise<RawResponse> {
    const url = new URL(spec.path, this.options.baseUrl);
    const transport = url.protocol === 'https:' ? https : http;
    const agent = url.protocol === 'https:' ? this.#httpsAgent : this.#httpAgent;
    return await new Promise((resolve, reject) => {
      let settled = false;
      const request = transport.request(url, {
        method: spec.method,
        headers: spec.headers,
        agent,
        ...(url.protocol === 'https:' && this.options.servername ? { servername: this.options.servername } : {}),
      }, (response) => {
        const chunks: Buffer[] = [];
        let total = 0;
        response.on('data', (chunk) => {
          const bytes = Buffer.from(chunk);
          total += bytes.byteLength;
          if (total > this.options.maxResponseBytes) {
            response.destroy();
            if (!settled) {
              settled = true;
              clearTimeout(timer);
              reject(new ServiceWireClientError('response-too-large', 'response exceeds configured limit', []));
            }
            return;
          }
          chunks.push(bytes);
        });
        response.on('end', () => {
          if (settled) return;
          settled = true;
          clearTimeout(timer);
          resolve({
            status: response.statusCode ?? 0,
            headers: response.headers,
            body: Buffer.concat(chunks, total),
          });
        });
        response.on('error', (error) => {
          if (settled) return;
          settled = true;
          clearTimeout(timer);
          reject(error);
        });
      });
      const timer = setTimeout(() => {
        if (settled) return;
        settled = true;
        request.destroy();
        reject(new ServiceWireClientError('deadline', 'request deadline expired', []));
      }, Math.max(1, Math.ceil(remainingMs)));
      request.on('error', (error) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        reject(error);
      });
      if (spec.body) request.write(spec.body);
      request.end();
    });
  }

  close(): void {
    if (this.#closed) return;
    this.#closed = true;
    this.#httpAgent.destroy();
    this.#httpsAgent.destroy();
  }
}
