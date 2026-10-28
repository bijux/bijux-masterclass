import http from 'node:http';
import https from 'node:https';
import { performance } from 'node:perf_hooks';

export interface AttemptRecord {
  readonly number: number;
  readonly url: string;
  readonly outcome: 'response' | 'error' | 'deadline';
  readonly status?: number;
  readonly code?: string;
}

export interface ClientResponse {
  readonly status: number;
  readonly headers: http.IncomingHttpHeaders;
  readonly body: Buffer;
  readonly attempts: readonly AttemptRecord[];
}

export class ClientError extends Error {
  constructor(
    readonly code: 'DEADLINE' | 'RESPONSE_TOO_LARGE' | 'REDIRECT' | 'TRANSPORT' | 'CLOSED',
    message: string,
    readonly attempts: readonly AttemptRecord[],
  ) {
    super(message);
    this.name = 'ClientError';
  }
}

export class DeadlineHttpClient {
  readonly #httpAgent: http.Agent;
  readonly #httpsAgent: https.Agent;
  #closed = false;

  constructor(readonly options: {
    readonly maxSockets: number;
    readonly maxResponseBytes: number;
    readonly maxAttempts: number;
    readonly allowSameOriginRedirects?: boolean;
    readonly ca?: Buffer;
  }) {
    this.#httpAgent = new http.Agent({ keepAlive: true, maxSockets: options.maxSockets, maxFreeSockets: options.maxSockets });
    this.#httpsAgent = new https.Agent({
      keepAlive: true,
      maxSockets: options.maxSockets,
      maxFreeSockets: options.maxSockets,
      ...(options.ca ? { ca: options.ca } : {}),
    });
  }

  async request(spec: {
    readonly url: URL;
    readonly method?: string;
    readonly headers?: Readonly<Record<string, string>>;
    readonly body?: Buffer;
    readonly budgetMs: number;
    readonly retry?: boolean;
    readonly signal?: AbortSignal;
  }): Promise<ClientResponse> {
    if (this.#closed) throw new ClientError('CLOSED', 'client is closed', []);
    const method = spec.method ?? 'GET';
    const deadline = performance.now() + spec.budgetMs;
    const attempts: AttemptRecord[] = [];
    const body = spec.body;
    const canRetry = spec.retry === true && (
      method === 'GET' || method === 'HEAD' ||
      (method === 'POST' && spec.headers?.['idempotency-key'] !== undefined && body !== undefined)
    );
    let current = new URL(spec.url);
    let redirects = 0;

    for (let number = 1; number <= this.options.maxAttempts; number += 1) {
      const remaining = deadline - performance.now();
      if (remaining <= 0) throw new ClientError('DEADLINE', 'operation deadline expired', attempts);
      try {
        const response = await this.attempt({
          url: current,
          method,
          remainingMs: remaining,
          ...(spec.headers ? { headers: spec.headers } : {}),
          ...(body ? { body } : {}),
          ...(spec.signal ? { signal: spec.signal } : {}),
        });
        attempts.push({ number, url: current.toString(), outcome: 'response', status: response.status });

        if ([301, 302, 303, 307, 308].includes(response.status) && response.headers.location) {
          const next = new URL(response.headers.location, current);
          if (!this.options.allowSameOriginRedirects || next.origin !== current.origin || redirects >= 3) {
            throw new ClientError('REDIRECT', 'redirect rejected by policy', attempts);
          }
          if (method !== 'GET' && method !== 'HEAD' && response.status !== 307 && response.status !== 308) {
            throw new ClientError('REDIRECT', 'method-changing redirect rejected', attempts);
          }
          current = next;
          redirects += 1;
          number -= 1;
          continue;
        }

        return { ...response, attempts };
      } catch (error) {
        if (error instanceof ClientError) throw error;
        const maybeCode = error instanceof Error ? (error as NodeJS.ErrnoException).code : undefined;
        const code = typeof maybeCode === 'string' ? maybeCode : 'ERROR';
        attempts.push({ number, url: current.toString(), outcome: 'error', code });
        if (!canRetry || number >= this.options.maxAttempts || performance.now() >= deadline) {
          throw new ClientError('TRANSPORT', 'request failed', attempts);
        }
      }
    }
    throw new ClientError('TRANSPORT', 'attempts exhausted', attempts);
  }

  private async attempt(spec: {
    readonly url: URL;
    readonly method: string;
    readonly headers?: Readonly<Record<string, string>>;
    readonly body?: Buffer;
    readonly remainingMs: number;
    readonly signal?: AbortSignal;
  }): Promise<Omit<ClientResponse, 'attempts'>> {
    const transport = spec.url.protocol === 'https:' ? https : http;
    const agent = spec.url.protocol === 'https:' ? this.#httpsAgent : this.#httpAgent;
    return await new Promise((resolve, reject) => {
      let settled = false;
      const request = transport.request(spec.url, {
        method: spec.method,
        agent,
        ...(spec.headers ? { headers: spec.headers } : {}),
        ...(spec.signal ? { signal: spec.signal } : {}),
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
              reject(new ClientError('RESPONSE_TOO_LARGE', 'response exceeds limit', []));
            }
            return;
          }
          chunks.push(bytes);
        });
        response.on('end', () => {
          if (settled) return;
          settled = true;
          clearTimeout(timer);
          resolve({ status: response.statusCode ?? 0, headers: response.headers, body: Buffer.concat(chunks, total) });
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
        reject(new ClientError('DEADLINE', 'operation deadline expired', []));
      }, Math.max(1, Math.ceil(spec.remainingMs)));
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
