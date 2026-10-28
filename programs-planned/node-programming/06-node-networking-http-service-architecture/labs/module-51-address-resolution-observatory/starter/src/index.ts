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

  remainingMs(): number {
    return Math.max(0, this.#at - this.#clock.nowMs());
  }
}
