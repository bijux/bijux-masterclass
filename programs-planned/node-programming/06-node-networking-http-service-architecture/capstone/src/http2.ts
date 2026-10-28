import http2 from 'node:http2';
import { once } from 'node:events';
import { randomUUID } from 'node:crypto';
import type { ServiceLimits } from './config.js';
import { dispatchFinite, type FiniteHttpRequest } from './http-shared.js';
import { ServiceProblem, toProblem } from './errors.js';
import type { ServiceWireApplication } from './service.js';

const { NGHTTP2_CANCEL } = http2.constants;

function headersMap(
  headers: http2.IncomingHttpHeaders,
): ReadonlyMap<string, string | readonly string[]> {
  const result = new Map<string, string | readonly string[]>();
  for (const [name, value] of Object.entries(headers)) {
    if (name.startsWith(':') || value === undefined) continue;
    if (typeof value === 'string') result.set(name.toLowerCase(), value);
    else if (Array.isArray(value)) result.set(name.toLowerCase(), value);
  }
  return result;
}

export async function startHttp2Server(options: {
  readonly application: ServiceWireApplication;
  readonly limits: ServiceLimits;
  readonly host: string;
  readonly port: number;
}): Promise<{
  readonly authority: string;
  readonly sessions: () => number;
  readonly streams: () => number;
  close(graceMs?: number): Promise<void>;
}> {
  const sessions = new Set<http2.ServerHttp2Session>();
  const streams = new Set<http2.ServerHttp2Stream>();
  let activeRequests = 0;
  let quiescing = false;
  let closePromise: Promise<void> | undefined;
  const server = http2.createServer({
    settings: { maxConcurrentStreams: options.limits.maxHttp2Streams },
  });

  server.on('session', (session) => {
    if (sessions.size >= options.limits.maxHttp2Sessions || quiescing) {
      session.destroy();
      return;
    }
    sessions.add(session);
    session.on('error', () => {});
    session.once('close', () => sessions.delete(session));
  });

  server.on('stream', (stream: http2.ServerHttp2Stream, incoming: http2.IncomingHttpHeaders) => {
    streams.add(stream);
    stream.on('error', () => {});
    stream.once('close', () => streams.delete(stream));
    activeRequests += 1;
    const finish = () => { activeRequests -= 1; };
    stream.once('close', finish);

    const method = incoming[':method'];
    const path = incoming[':path'];
    if (typeof method !== 'string' || typeof path !== 'string') {
      stream.respond({ ':status': 400, 'content-length': '0' });
      stream.end();
      return;
    }
    const requestIdValue = incoming['x-request-id'];
    const requestId = typeof requestIdValue === 'string' && /^[A-Za-z0-9._:-]{1,64}$/.test(requestIdValue)
      ? requestIdValue
      : randomUUID();
    const chunks: Buffer[] = [];
    let total = 0;
    let terminal = false;

    stream.on('data', (chunk: Buffer | string) => {
      if (terminal) return;
      const bytes = Buffer.from(chunk);
      total += bytes.byteLength;
      if (total > options.limits.maxRequestBodyBytes) {
        terminal = true;
        const problem = toProblem(
          new ServiceProblem('BODY_TOO_LARGE', 413, 'Request body exceeds limit'),
          requestId,
        );
        const body = Buffer.from(JSON.stringify(problem));
        stream.respond({
          ':status': 413,
          'content-type': 'application/problem+json',
          'content-length': String(body.byteLength),
          'x-request-id': requestId,
        });
        stream.end(body);
        return;
      }
      chunks.push(bytes);
    });

    stream.on('end', () => {
      if (terminal || stream.closed || stream.destroyed) return;
      terminal = true;
      const finiteRequest: FiniteHttpRequest = {
        method,
        url: new URL(path, 'http://servicewire.invalid'),
        headers: headersMap(incoming),
        body: Buffer.concat(chunks, total),
        requestId,
      };
      const finite = dispatchFinite(options.application, finiteRequest);
      stream.respond({
        ':status': finite.status,
        ...finite.headers,
        'x-request-id': requestId,
      });
      stream.end(finite.omitBody ? undefined : finite.body);
    });
  });

  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen({ host: options.host, port: options.port }, () => {
      server.off('error', reject);
      resolve();
    });
  });
  const address = server.address();
  if (address === null || typeof address === 'string') throw new Error('expected IP listener');

  return {
    authority: `http://${options.host}:${address.port}`,
    sessions: () => sessions.size,
    streams: () => streams.size,
    close: (graceMs = options.limits.shutdownGraceMs) => {
      if (closePromise) return closePromise;
      closePromise = (async () => {
        quiescing = true;
        const closed = new Promise<void>((resolve) => server.close(() => resolve()));
        for (const session of sessions) session.close();
        const deadline = Date.now() + graceMs;
        while ((activeRequests > 0 || streams.size > 0 || sessions.size > 0) && Date.now() < deadline) {
          await new Promise((resolve) => setTimeout(resolve, 5));
        }
        for (const stream of streams) {
          if (!stream.closed && !stream.destroyed) stream.close(NGHTTP2_CANCEL);
        }
        for (const session of sessions) session.destroy();
        await closed;
        if (sessions.size > 0) {
          await Promise.all([...sessions].map((session) => once(session, 'close').then(() => undefined)));
        }
      })();
      return closePromise;
    },
  };
}
