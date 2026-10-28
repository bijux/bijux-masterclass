import dgram from 'node:dgram';
import { randomBytes } from 'node:crypto';
import { SERVICEWIRE_VERSION } from './version.js';

const NONCE = /^[0-9a-f]{32}$/;
const MAX_DATAGRAM_BYTES = 512;

export function createDiscoveryNonce(): string {
  return randomBytes(16).toString('hex');
}

export function encodeDiscoveryRequest(nonce: string): Buffer {
  if (!NONCE.test(nonce)) throw new Error('invalid discovery nonce');
  return Buffer.from(`SERVICEWIRE-DISCOVER-V1\t${nonce}`, 'ascii');
}

export function decodeDiscoveryRequest(bytes: Uint8Array): string {
  if (bytes.byteLength > MAX_DATAGRAM_BYTES) throw new Error('discovery datagram too large');
  const [tag, nonce, extra] = Buffer.from(bytes).toString('ascii').split('\t');
  if (tag !== 'SERVICEWIRE-DISCOVER-V1' || extra !== undefined || nonce === undefined || !NONCE.test(nonce)) {
    throw new Error('invalid discovery request');
  }
  return nonce;
}

export function encodeDiscoveryResponse(nonce: string, advertisedUrl: string): Buffer {
  if (!NONCE.test(nonce)) throw new Error('invalid discovery nonce');
  const url = new URL(advertisedUrl).toString();
  const bytes = Buffer.from(
    `SERVICEWIRE-HERE-V1\t${nonce}\t${url}\t${SERVICEWIRE_VERSION}`,
    'utf8',
  );
  if (bytes.byteLength > MAX_DATAGRAM_BYTES) throw new Error('discovery response too large');
  return bytes;
}

export function decodeDiscoveryResponse(bytes: Uint8Array): {
  readonly nonce: string;
  readonly url: string;
  readonly version: string;
} {
  if (bytes.byteLength > MAX_DATAGRAM_BYTES) throw new Error('discovery datagram too large');
  const [tag, nonce, url, version, extra] = Buffer.from(bytes).toString('utf8').split('\t');
  if (
    tag !== 'SERVICEWIRE-HERE-V1' ||
    extra !== undefined ||
    nonce === undefined ||
    url === undefined ||
    version === undefined ||
    !NONCE.test(nonce)
  ) {
    throw new Error('invalid discovery response');
  }
  return { nonce, url: new URL(url).toString(), version };
}

export async function startDiscoveryServer(options: {
  readonly host: string;
  readonly port: number;
  readonly advertisedUrl: string;
}): Promise<{
  readonly host: string;
  readonly port: number;
  close(): Promise<void>;
}> {
  const socket = dgram.createSocket('udp4');
  socket.on('message', (message, peer) => {
    try {
      const nonce = decodeDiscoveryRequest(message);
      const response = encodeDiscoveryResponse(nonce, options.advertisedUrl);
      socket.send(response, peer.port, peer.address);
    } catch {
      // Unrelated malformed local datagrams are ignored.
    }
  });
  await new Promise<void>((resolve, reject) => {
    socket.once('error', reject);
    socket.bind(options.port, options.host, () => {
      socket.off('error', reject);
      resolve();
    });
  });
  const address = socket.address();
  let closed = false;
  return {
    host: address.address,
    port: address.port,
    close: async () => {
      if (closed) return;
      closed = true;
      await new Promise<void>((resolve) => socket.close(() => resolve()));
    },
  };
}

export async function discoverService(options: {
  readonly host: string;
  readonly port: number;
  readonly budgetMs: number;
  readonly attempts?: number;
}): Promise<{ readonly url: string; readonly version: string; readonly attempts: number }> {
  const nonce = createDiscoveryNonce();
  const socket = dgram.createSocket('udp4');
  const deadline = Date.now() + options.budgetMs;
  const maxAttempts = options.attempts ?? 3;
  return await new Promise((resolve, reject) => {
    let attempt = 0;
    let settled = false;
    let deadlineTimer: NodeJS.Timeout | undefined;
    let retryTimer: NodeJS.Timeout | undefined;
    const finish = (
      error?: Error,
      value?: { readonly url: string; readonly version: string; readonly attempts: number },
    ) => {
      if (settled) return;
      settled = true;
      if (deadlineTimer) clearTimeout(deadlineTimer);
      if (retryTimer) clearTimeout(retryTimer);
      socket.removeAllListeners();
      socket.close(() => {
        if (error) reject(error);
        else if (value) resolve(value);
        else reject(new Error('discovery failed'));
      });
    };
    const send = () => {
      if (Date.now() >= deadline || attempt >= maxAttempts) {
        finish(new Error('discovery deadline expired'));
        return;
      }
      attempt += 1;
      socket.send(encodeDiscoveryRequest(nonce), options.port, options.host);
      retryTimer = setTimeout(send, Math.min(50 * attempt, Math.max(1, deadline - Date.now())));
    };
    socket.on('message', (message, peer) => {
      if (peer.address !== options.host && options.host !== 'localhost') return;
      try {
        const response = decodeDiscoveryResponse(message);
        if (response.nonce !== nonce) return;
        finish(undefined, { url: response.url, version: response.version, attempts: attempt });
      } catch {
        // Ignore unrelated traffic.
      }
    });
    socket.once('error', (error) => finish(error));
    deadlineTimer = setTimeout(() => finish(new Error('discovery deadline expired')), options.budgetMs);
    socket.bind(0, '127.0.0.1', send);
  });
}
