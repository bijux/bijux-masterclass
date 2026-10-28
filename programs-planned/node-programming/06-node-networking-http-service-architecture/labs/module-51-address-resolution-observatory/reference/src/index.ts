import net from 'node:net';
import { performance } from 'node:perf_hooks';

export interface Clock {
  nowMs(): number;
}

export const systemClock: Clock = {
  nowMs: () => performance.now(),
};

export interface ServiceEndpoint {
  readonly scheme: 'http:' | 'https:';
  readonly hostname: string;
  readonly port: number;
}

export interface AddressCandidate {
  readonly address: string;
  readonly family: 4 | 6;
}

export interface AttemptRecord {
  readonly candidate: AddressCandidate;
  readonly elapsedMs: number;
  readonly outcome: 'failed' | 'connected';
  readonly code?: string;
}

export interface ConnectionHandle {
  readonly localAddress: string;
  readonly peerAddress: string;
  close(): void;
}

export type Resolver = (hostname: string) => Promise<readonly AddressCandidate[]>;

export type Connector = (
  endpoint: ServiceEndpoint,
  candidate: AddressCandidate,
  remainingMs: number,
  signal?: AbortSignal,
) => Promise<ConnectionHandle>;

export function parseEndpoint(text: string): ServiceEndpoint {
  const url = new URL(text);
  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    throw new Error('unsupported scheme');
  }
  if (url.username || url.password || url.hash) {
    throw new Error('credentials and fragments are not supported');
  }
  const port = url.port === '' ? (url.protocol === 'https:' ? 443 : 80) : Number(url.port);
  if (!Number.isInteger(port) || port < 1 || port > 65_535) {
    throw new Error('invalid port');
  }
  return { scheme: url.protocol, hostname: url.hostname, port };
}

export class Deadline {
  readonly #at: number;
  readonly #clock: Clock;

  constructor(budgetMs: number, clock: Clock = systemClock) {
    if (!Number.isFinite(budgetMs) || budgetMs <= 0) {
      throw new RangeError('budgetMs must be positive and finite');
    }
    this.#clock = clock;
    this.#at = clock.nowMs() + budgetMs;
  }

  nowMs(): number {
    return this.#clock.nowMs();
  }

  remainingMs(): number {
    return Math.max(0, this.#at - this.#clock.nowMs());
  }

  expired(): boolean {
    return this.remainingMs() === 0;
  }
}

export class ConnectionExhaustedError extends Error {
  constructor(readonly attempts: readonly AttemptRecord[]) {
    super('all address candidates failed or the deadline expired');
    this.name = 'ConnectionExhaustedError';
  }
}

function stableCode(error: unknown): string {
  if (error instanceof Error) {
    const value = (error as NodeJS.ErrnoException).code;
    return typeof value === 'string' ? value : error.name;
  }
  return 'UNKNOWN';
}

export async function planConnection(
  endpoint: ServiceEndpoint,
  resolver: Resolver,
  connector: Connector,
  options: {
    readonly budgetMs: number;
    readonly clock?: Clock;
    readonly signal?: AbortSignal;
  },
): Promise<{
  readonly endpoint: ServiceEndpoint;
  readonly candidate: AddressCandidate;
  readonly connection: ConnectionHandle;
  readonly attempts: readonly AttemptRecord[];
}> {
  const deadline = new Deadline(options.budgetMs, options.clock ?? systemClock);
  if (options.signal?.aborted) {
    throw options.signal.reason instanceof Error
      ? options.signal.reason
      : new Error('operation cancelled');
  }
  const candidates = await resolver(endpoint.hostname);
  const attempts: AttemptRecord[] = [];

  for (const candidate of candidates) {
    const remaining = deadline.remainingMs();
    if (remaining <= 0) break;
    if (options.signal?.aborted) {
      throw options.signal.reason instanceof Error
        ? options.signal.reason
        : new Error('operation cancelled');
    }
    const started = deadline.nowMs();
    try {
      const connection = await connector(endpoint, candidate, remaining, options.signal);
      attempts.push({
        candidate,
        elapsedMs: Math.max(0, deadline.nowMs() - started),
        outcome: 'connected',
      });
      return { endpoint, candidate, connection, attempts };
    } catch (error) {
      attempts.push({
        candidate,
        elapsedMs: Math.max(0, deadline.nowMs() - started),
        outcome: 'failed',
        code: stableCode(error),
      });
    }
  }

  throw new ConnectionExhaustedError(attempts);
}

export async function listenEphemeral(
  host = '127.0.0.1',
): Promise<{
  readonly server: net.Server;
  readonly address: string;
  readonly port: number;
  close(): Promise<void>;
}> {
  const server = net.createServer();
  await new Promise<void>((resolve, reject) => {
    const onError = (error: Error) => {
      server.off('listening', onListening);
      reject(error);
    };
    const onListening = () => {
      server.off('error', onError);
      resolve();
    };
    server.once('error', onError);
    server.once('listening', onListening);
    server.listen({ host, port: 0 });
  });

  const observed = server.address();
  if (observed === null || typeof observed === 'string') {
    server.close();
    throw new Error('expected an IP listener address');
  }

  return {
    server,
    address: observed.address,
    port: observed.port,
    close: async () => {
      if (!server.listening) return;
      await new Promise<void>((resolve, reject) => {
        server.close((error) => error ? reject(error) : resolve());
      });
    },
  };
}
