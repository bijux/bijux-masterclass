import tls from 'node:tls';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { once } from 'node:events';

export interface TlsFixtures {
  readonly ca: Buffer;
  readonly cert: Buffer;
  readonly key: Buffer;
}

export async function loadFixtures(directory = join(process.cwd(), 'fixtures')): Promise<TlsFixtures> {
  const [ca, cert, key] = await Promise.all([
    readFile(join(directory, 'ca-cert.pem')),
    readFile(join(directory, 'server-cert.pem')),
    readFile(join(directory, 'server-key.pem')),
  ]);
  return { ca, cert, key };
}

export async function startTlsEchoServer(
  fixtures: TlsFixtures,
  options: { readonly maxBytes: number; readonly alpn?: readonly string[] },
): Promise<{
  readonly host: string;
  readonly port: number;
  readonly activeSockets: () => number;
  close(graceMs?: number): Promise<void>;
}> {
  const sockets = new Set<tls.TLSSocket>();
  const server = tls.createServer({
    key: fixtures.key,
    cert: fixtures.cert,
    ALPNProtocols: options.alpn ?? ['http/1.1'],
  }, (socket) => {
    sockets.add(socket);
    let total = 0;
    socket.on('data', (chunk) => {
      const bytes = Buffer.from(chunk);
      total += bytes.byteLength;
      if (total > options.maxBytes) {
        socket.destroy(new Error('payload exceeds limit'));
        return;
      }
      socket.write(bytes);
    });
    socket.on('end', () => socket.end());
    socket.on('error', () => {});
    socket.once('close', () => sockets.delete(socket));
  });

  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen({ host: '127.0.0.1', port: 0 }, () => {
      server.off('error', reject);
      resolve();
    });
  });
  const observed = server.address();
  if (observed === null || typeof observed === 'string') throw new Error('expected IP listener');

  return {
    host: observed.address,
    port: observed.port,
    activeSockets: () => sockets.size,
    close: async (graceMs = 100) => {
      await new Promise<void>((resolve) => server.close(() => resolve()));
      const deadline = Date.now() + graceMs;
      while (sockets.size > 0 && Date.now() < deadline) {
        await new Promise((resolve) => setTimeout(resolve, 5));
      }
      for (const socket of sockets) socket.destroy();
      if (sockets.size > 0) await Promise.all([...sockets].map((socket) => once(socket, 'close').then(() => undefined)));
    },
  };
}

export async function connectTls(options: {
  readonly host: string;
  readonly port: number;
  readonly servername: string;
  readonly ca: Buffer;
  readonly requiredAlpn?: string;
  readonly budgetMs: number;
  readonly signal?: AbortSignal;
}): Promise<{
  readonly socket: tls.TLSSocket;
  readonly alpnProtocol: string;
  readonly peerFingerprint256: string | undefined;
}> {
  return await new Promise((resolve, reject) => {
    let settled = false;
    const socket = tls.connect({
      host: options.host,
      port: options.port,
      servername: options.servername,
      ca: options.ca,
      ALPNProtocols: options.requiredAlpn ? [options.requiredAlpn] : ['http/1.1'],
      rejectUnauthorized: true,
    });
    const cleanup = () => {
      clearTimeout(timer);
      options.signal?.removeEventListener('abort', onAbort);
      socket.off('error', onError);
      socket.off('secureConnect', onSecure);
    };
    const fail = (error: Error) => {
      if (settled) return;
      settled = true;
      cleanup();
      socket.destroy();
      reject(error);
    };
    const onAbort = () => fail(options.signal?.reason instanceof Error ? options.signal.reason : new Error('cancelled'));
    const onError = (error: Error) => fail(error);
    const onSecure = () => {
      if (options.requiredAlpn && socket.alpnProtocol !== options.requiredAlpn) {
        fail(new Error(`required ALPN ${options.requiredAlpn} was not negotiated`));
        return;
      }
      settled = true;
      cleanup();
      const peer = socket.getPeerCertificate();
      resolve({
        socket,
        alpnProtocol: typeof socket.alpnProtocol === 'string' ? socket.alpnProtocol : '',
        peerFingerprint256: peer.fingerprint256,
      });
    };
    const timer = setTimeout(() => fail(new Error('TLS deadline expired')), options.budgetMs);
    options.signal?.addEventListener('abort', onAbort, { once: true });
    socket.once('error', onError);
    socket.once('secureConnect', onSecure);
  });
}
