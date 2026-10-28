import http2 from 'node:http2';
import { once } from 'node:events';

const { NGHTTP2_CANCEL } = http2.constants;

export interface H2Response {
  readonly status: number;
  readonly body: Buffer;
}

export async function startHttp2Service(options: {
  readonly maxBodyBytes: number;
  readonly maxSessions: number;
  readonly maxStreams: number;
}): Promise<{
  readonly authority: string;
  readonly sessions: () => number;
  readonly streams: () => number;
  close(graceMs?: number): Promise<void>;
}> {
  const sessions = new Set<http2.ServerHttp2Session>();
  const streams = new Set<http2.ServerHttp2Stream>();
  const server = http2.createServer({
    settings: { maxConcurrentStreams: options.maxStreams },
  });

  server.on('session', (session) => {
    if (sessions.size >= options.maxSessions) {
      session.destroy();
      return;
    }
    sessions.add(session);
    session.once('close', () => sessions.delete(session));
    session.on('error', () => {});
  });

  server.on('stream', (stream: http2.ServerHttp2Stream, headers: http2.IncomingHttpHeaders) => {
    streams.add(stream);
    stream.once('close', () => streams.delete(stream));
    stream.on('error', () => {});
    const method = headers[':method'];
    const pathText = headers[':path'];
    if (typeof method !== 'string' || typeof pathText !== 'string') {
      stream.respond({ ':status': 400 });
      stream.end();
      return;
    }

    const chunks: Buffer[] = [];
    let total = 0;
    let overLimit = false;
    stream.on('data', (chunk: Buffer | string) => {
      if (overLimit) return;
      const bytes = Buffer.from(chunk);
      total += bytes.byteLength;
      if (total > options.maxBodyBytes) {
        overLimit = true;
        stream.respond({ ':status': 413, 'content-length': '0' });
        stream.end();
        return;
      }
      chunks.push(bytes);
    });
    stream.on('end', () => {
      if (overLimit || stream.destroyed || stream.closed) return;
      const url = new URL(pathText, 'http://h2.invalid');
      if (method === 'GET' && url.pathname === '/health') {
        const body = Buffer.from('{"ok":true}');
        stream.respond({ ':status': 200, 'content-type': 'application/json', 'content-length': String(body.byteLength) });
        stream.end(body);
        return;
      }
      if (method === 'POST' && url.pathname === '/echo') {
        const body = Buffer.concat(chunks, total);
        stream.respond({ ':status': 200, 'content-type': 'application/octet-stream', 'content-length': String(body.byteLength) });
        stream.end(body);
        return;
      }
      if (method === 'GET' && url.pathname === '/slow') {
        const ms = Number(url.searchParams.get('ms') ?? '0');
        setTimeout(() => {
          if (stream.destroyed || stream.closed) return;
          const body = Buffer.from(String(ms));
          stream.respond({ ':status': 200, 'content-length': String(body.byteLength) });
          stream.end(body);
        }, Number.isFinite(ms) ? Math.max(0, Math.min(100, ms)) : 0);
        return;
      }
      stream.respond({ ':status': 404, 'content-length': '0' });
      stream.end();
    });
  });

  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      server.off('error', reject);
      resolve();
    });
  });
  const observed = server.address();
  if (observed === null || typeof observed === 'string') throw new Error('address');
  return {
    authority: `http://127.0.0.1:${observed.port}`,
    sessions: () => sessions.size,
    streams: () => streams.size,
    close: async (graceMs = 100) => {
      const closed = new Promise<void>((resolve) => server.close(() => resolve()));
      for (const session of sessions) session.close();
      const deadline = Date.now() + graceMs;
      while ((sessions.size > 0 || streams.size > 0) && Date.now() < deadline) {
        await new Promise((resolve) => setTimeout(resolve, 5));
      }
      for (const stream of streams) {
        if (!stream.closed && !stream.destroyed) stream.close(NGHTTP2_CANCEL);
      }
      const closing = [...sessions].map((session) => once(session, 'close').then(() => undefined));
      for (const session of sessions) session.destroy();
      await Promise.allSettled(closing);
      await closed;
    },
  };
}

export async function h2Request(
  session: http2.ClientHttp2Session,
  options: { readonly method: string; readonly path: string; readonly body?: Buffer; readonly reset?: boolean },
): Promise<H2Response> {
  return await new Promise((resolve, reject) => {
    const stream = session.request({ ':method': options.method, ':path': options.path });
    const chunks: Buffer[] = [];
    let status = 0;
    stream.on('response', (headers) => { status = Number(headers[':status'] ?? 0); });
    stream.on('data', (chunk) => chunks.push(Buffer.from(chunk)));
    let settled = false;
    stream.on('end', () => {
      if (settled) return;
      settled = true;
      resolve({ status, body: Buffer.concat(chunks) });
    });
    stream.on('error', (error) => {
      if (settled) return;
      settled = true;
      reject(error);
    });
    if (options.reset) {
      settled = true;
      stream.close(NGHTTP2_CANCEL);
      reject(new Error('stream reset by client'));
      return;
    }
    stream.end(options.body);
  });
}
