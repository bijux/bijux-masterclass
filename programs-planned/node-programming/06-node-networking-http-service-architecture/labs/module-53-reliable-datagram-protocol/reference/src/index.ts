import dgram from 'node:dgram';
import { randomBytes } from 'node:crypto';

const NONCE = /^[0-9a-f]{32}$/;
const MAX_DATAGRAM = 512;

export interface DiscoveryRequest { readonly nonce: string; }
export interface DiscoveryResponse {
  readonly nonce: string;
  readonly url: string;
  readonly version: string;
}

export function createNonce(): string {
  return randomBytes(16).toString('hex');
}

export function encodeRequest(value: DiscoveryRequest): Buffer {
  if (!NONCE.test(value.nonce)) throw new Error('invalid nonce');
  return Buffer.from(`DISCOVER-V1\t${value.nonce}`, 'ascii');
}

export function decodeRequest(bytes: Uint8Array): DiscoveryRequest {
  if (bytes.byteLength > MAX_DATAGRAM) throw new Error('datagram too large');
  const text = Buffer.from(bytes).toString('ascii');
  const [tag, nonce, extra] = text.split('\t');
  if (tag !== 'DISCOVER-V1' || extra !== undefined || nonce === undefined || !NONCE.test(nonce)) {
    throw new Error('invalid request');
  }
  return { nonce };
}

export function encodeResponse(value: DiscoveryResponse): Buffer {
  if (!NONCE.test(value.nonce)) throw new Error('invalid nonce');
  const url = new URL(value.url).toString();
  const bytes = Buffer.from(`HERE-V1\t${value.nonce}\t${url}\t${value.version}`, 'utf8');
  if (bytes.byteLength > MAX_DATAGRAM) throw new Error('response too large');
  return bytes;
}

export function decodeResponse(bytes: Uint8Array): DiscoveryResponse {
  if (bytes.byteLength > MAX_DATAGRAM) throw new Error('datagram too large');
  const [tag, nonce, url, version, extra] = Buffer.from(bytes).toString('utf8').split('\t');
  if (tag !== 'HERE-V1' || extra !== undefined || nonce === undefined || url === undefined || version === undefined) {
    throw new Error('invalid response');
  }
  if (!NONCE.test(nonce)) throw new Error('invalid nonce');
  return { nonce, url: new URL(url).toString(), version };
}

export class ReplayCache {
  readonly #entries = new Map<string, { readonly response: Buffer; readonly expiresAt: number }>();
  constructor(readonly maxEntries: number, readonly retentionMs: number) {
    if (!Number.isInteger(maxEntries) || maxEntries < 1) throw new RangeError('maxEntries');
    if (!Number.isFinite(retentionMs) || retentionMs <= 0) throw new RangeError('retentionMs');
  }
  get(key: string, now: number): Buffer | undefined {
    this.evict(now);
    const found = this.#entries.get(key);
    return found ? Buffer.from(found.response) : undefined;
  }
  set(key: string, response: Uint8Array, now: number): void {
    this.evict(now);
    if (!this.#entries.has(key) && this.#entries.size >= this.maxEntries) {
      const oldest = this.#entries.keys().next().value as string | undefined;
      if (oldest !== undefined) this.#entries.delete(oldest);
    }
    this.#entries.set(key, { response: Buffer.from(response), expiresAt: now + this.retentionMs });
  }
  size(now: number): number { this.evict(now); return this.#entries.size; }
  private evict(now: number): void {
    for (const [key, value] of this.#entries) if (value.expiresAt <= now) this.#entries.delete(key);
  }
}

export type Exchange = (
  request: Buffer,
  attempt: number,
  signal: AbortSignal,
) => Promise<readonly { readonly bytes: Buffer; readonly peer: string }[]>;

export async function requestWithRetry(
  exchange: Exchange,
  options: {
    readonly nonce: string;
    readonly expectedPeer: string;
    readonly budgetMs: number;
    readonly delaysMs: readonly number[];
    readonly now?: () => number;
    readonly sleep?: (ms: number, signal: AbortSignal) => Promise<void>;
    readonly signal?: AbortSignal;
  },
): Promise<{ readonly response: DiscoveryResponse; readonly attempts: number }> {
  const now = options.now ?? Date.now;
  const deadline = now() + options.budgetMs;
  const controller = new AbortController();
  const onAbort = () => controller.abort(options.signal?.reason);
  options.signal?.addEventListener('abort', onAbort, { once: true });
  const sleep = options.sleep ?? (async (ms, signal) => {
    await new Promise<void>((resolve, reject) => {
      const timer = setTimeout(resolve, ms);
      signal.addEventListener('abort', () => {
        clearTimeout(timer);
        reject(signal.reason);
      }, { once: true });
    });
  });
  try {
    const request = encodeRequest({ nonce: options.nonce });
    for (let attempt = 0; attempt <= options.delaysMs.length; attempt += 1) {
      if (controller.signal.aborted) throw controller.signal.reason;
      if (now() >= deadline) throw new Error('deadline');
      const packets = await exchange(request, attempt + 1, controller.signal);
      for (const packet of packets) {
        if (packet.peer !== options.expectedPeer) continue;
        try {
          const response = decodeResponse(packet.bytes);
          if (response.nonce === options.nonce) return { response, attempts: attempt + 1 };
        } catch {
          // Unrelated malformed traffic does not terminate the request.
        }
      }
      const delay = options.delaysMs[attempt];
      if (delay === undefined) break;
      const remaining = deadline - now();
      if (remaining <= 0 || delay >= remaining) break;
      await sleep(delay, controller.signal);
    }
    throw new Error('deadline or attempts exhausted');
  } finally {
    options.signal?.removeEventListener('abort', onAbort);
  }
}

export async function startResponder(options: {
  readonly host?: string;
  readonly url: string;
  readonly version: string;
}): Promise<{ readonly port: number; close(): Promise<void> }> {
  const socket = dgram.createSocket('udp4');
  socket.on('message', (message, peer) => {
    try {
      const request = decodeRequest(message);
      const response = encodeResponse({ nonce: request.nonce, url: options.url, version: options.version });
      socket.send(response, peer.port, peer.address);
    } catch {
      // Ignore unrelated malformed datagrams.
    }
  });
  await new Promise<void>((resolve, reject) => {
    socket.once('error', reject);
    socket.bind(0, options.host ?? '127.0.0.1', () => {
      socket.off('error', reject);
      resolve();
    });
  });
  const address = socket.address();
  return {
    port: address.port,
    close: async () => {
      await new Promise<void>((resolve) => socket.close(() => resolve()));
    },
  };
}
