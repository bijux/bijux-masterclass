import http from 'node:http';
import https from 'node:https';
import type net from 'node:net';
import { randomUUID } from 'node:crypto';
import { once } from 'node:events';
import type { ServiceLimits, TlsConfig } from './config.js';
import { ServiceProblem, toProblem } from './errors.js';
import { dispatchFinite, encodeSseEvent, type FiniteHttpRequest } from './http-shared.js';
import type { ServiceWireApplication } from './service.js';

function headerMap(headers: http.IncomingHttpHeaders): ReadonlyMap<string, string | readonly string[]> {
  const result = new Map<string, string | readonly string[]>();
  for (const [name, value] of Object.entries(headers)) {
    if (value !== undefined) result.set(name.toLowerCase(), value);
  }
  return result;
}

async function readBody(
  request: http.IncomingMessage,
  maxBytes: number,
): Promise<Buffer> {
  const declared = request.headers['content-length'];
  if (typeof declared === 'string') {
    const length = Number(declared);
    if (Number.isSafeInteger(length) && length > maxBytes) {
      throw new ServiceProblem('BODY_TOO_LARGE', 413, `Request body exceeds ${maxBytes} bytes`);
    }
  }
  const chunks: Buffer[] = [];
  let total = 0;
  for await (const chunk of request) {
    const bytes = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    total += bytes.byteLength;
    if (total > maxBytes) {
      throw new ServiceProblem('BODY_TOO_LARGE', 413, `Request body exceeds ${maxBytes} bytes`);
    }
    chunks.push(bytes);
  }
  return Buffer.concat(chunks, total);
}

function sendFinite(response: http.ServerResponse, finite: ReturnType<typeof dispatchFinite>): void {
  response.writeHead(finite.status, finite.headers);
  response.end(finite.omitBody ? undefined : finite.body);
}

function parseCursor(request: http.IncomingMessage, url: URL): number | undefined {
  const query = url.searchParams.get('after');
  const last = request.headers['last-event-id'];
  if (query !== null && typeof last === 'string') {
    throw new ServiceProblem('INVALID_REQUEST', 400, 'Use either after or Last-Event-ID, not both');
  }
  const raw = query ?? (typeof last === 'string' ? last : undefined);
  if (raw === undefined) return undefined;
  const value = Number(raw);
  if (!Number.isSafeInteger(value) || value < 0) {
    throw new ServiceProblem('INVALID_REQUEST', 400, 'Invalid event cursor');
  }
  return value;
}

function serveSse(
  request: http.IncomingMessage,
  response: http.ServerResponse,
  application: ServiceWireApplication,
  limits: ServiceLimits,
  responses: Set<http.ServerResponse>,
): void {
  const url = new URL(request.url ?? '/', 'http://servicewire.invalid');
  let subscription: ReturnType<typeof application.events.open>;
  const queue: Buffer[] = [];
  let queuedBytes = 0;
  let pressured = false;
  let closed = false;
  let heartbeat: ReturnType<typeof setInterval> | undefined;

  const cleanup = () => {
    if (closed) return;
    closed = true;
    if (heartbeat) clearInterval(heartbeat);
    subscription.dispose();
    responses.delete(response);
    queue.length = 0;
    queuedBytes = 0;
  };

  const flush = () => {
    if (closed || pressured) return;
    while (queue.length > 0) {
      const bytes = queue.shift();
      if (!bytes) break;
      queuedBytes -= bytes.byteLength;
      if (!response.write(bytes)) {
        pressured = true;
        response.once('drain', () => {
          pressured = false;
          flush();
        });
        break;
      }
    }
  };

  const enqueue = (bytes: Buffer) => {
    if (closed) return;
    if (queuedBytes + bytes.byteLength > limits.maxSubscriberQueueBytes) {
      cleanup();
      response.destroy(new Error('slow subscriber queue exceeded'));
      return;
    }
    queue.push(bytes);
    queuedBytes += bytes.byteLength;
    flush();
  };

  try {
    subscription = application.events.open(
      parseCursor(request, url),
      (event) => enqueue(encodeSseEvent(event)),
    );
  } catch (error) {
    const problem = toProblem(error, randomUUID());
    const body = Buffer.from(JSON.stringify(problem));
    response.writeHead(problem.status, {
      'content-type': 'application/problem+json',
      'content-length': String(body.byteLength),
    });
    response.end(body);
    return;
  }

  response.writeHead(200, {
    'content-type': 'text/event-stream; charset=utf-8',
    'cache-control': 'no-cache',
    connection: 'keep-alive',
  });
  responses.add(response);
  for (const event of subscription.replay) enqueue(encodeSseEvent(event));
  heartbeat = setInterval(() => enqueue(Buffer.from(': heartbeat\n\n')), limits.heartbeatMs);
  response.once('close', cleanup);
  response.once('error', cleanup);
}

export async function startHttp1Server(options: {
  readonly application: ServiceWireApplication;
  readonly limits: ServiceLimits;
  readonly host: string;
  readonly port: number;
  readonly tls?: TlsConfig;
}): Promise<{
  readonly scheme: 'http' | 'https';
  readonly host: string;
  readonly port: number;
  readonly url: string;
  readonly activeRequests: () => number;
  readonly activeSockets: () => number;
  readonly sseResponses: () => number;
  close(graceMs?: number): Promise<void>;
}> {
  const sockets = new Set<net.Socket>();
  const sseResponses = new Set<http.ServerResponse>();
  let activeRequests = 0;
  let quiescing = false;

  const listener: http.RequestListener = async (request, response) => {
    const url = new URL(request.url ?? '/', 'http://servicewire.invalid');
    if (request.method === 'GET' && url.pathname === '/v1/events') {
      if (quiescing) {
        const problem = toProblem(new ServiceProblem('NOT_READY', 503, 'Service is quiescing'), randomUUID());
        const body = Buffer.from(JSON.stringify(problem));
        response.writeHead(503, {
          'content-type': 'application/problem+json',
          'content-length': String(body.byteLength),
        });
        response.end(body);
        return;
      }
      serveSse(request, response, options.application, options.limits, sseResponses);
      return;
    }

    activeRequests += 1;
    try {
      const headers = headerMap(request.headers);
      const requestIdValue = headers.get('x-request-id');
      const requestId = typeof requestIdValue === 'string' && /^[A-Za-z0-9._:-]{1,64}$/.test(requestIdValue)
        ? requestIdValue
        : randomUUID();
      const body = await readBody(request, options.limits.maxRequestBodyBytes);
      const finiteRequest: FiniteHttpRequest = {
        method: request.method ?? '',
        url,
        headers,
        body,
        requestId,
      };
      const finite = dispatchFinite(options.application, finiteRequest);
      response.setHeader('x-request-id', requestId);
      sendFinite(response, finite);
    } catch (error) {
      if (!response.headersSent) {
        const problem = toProblem(error, randomUUID());
        const body = Buffer.from(JSON.stringify(problem));
        response.writeHead(problem.status, {
          'content-type': 'application/problem+json',
          'content-length': String(body.byteLength),
        });
        response.end(body);
      } else {
        response.destroy();
      }
    } finally {
      activeRequests -= 1;
    }
  };

  const server = options.tls
    ? https.createServer({
        key: options.tls.key,
        cert: options.tls.cert,
        ...(options.tls.ca ? { ca: [...options.tls.ca] } : {}),
        ALPNProtocols: ['http/1.1'],
      }, listener)
    : http.createServer(listener);

  server.maxConnections = options.limits.maxConnections;
  server.headersTimeout = 5_000;
  server.requestTimeout = 10_000;
  server.keepAliveTimeout = 2_000;
  server.on('connection', (socket) => {
    sockets.add(socket);
    socket.once('close', () => sockets.delete(socket));
  });

  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen({ host: options.host, port: options.port }, () => {
      server.off('error', reject);
      resolve();
    });
  });
  const address = server.address();
  if (address === null || typeof address === 'string') {
    server.close();
    throw new Error('expected IP listener');
  }
  const scheme = options.tls ? 'https' : 'http';
  let closePromise: Promise<void> | undefined;
  return {
    scheme,
    host: address.address,
    port: address.port,
    url: `${scheme}://${options.host}:${address.port}`,
    activeRequests: () => activeRequests,
    activeSockets: () => sockets.size,
    sseResponses: () => sseResponses.size,
    close: (graceMs = options.limits.shutdownGraceMs) => {
      if (closePromise) return closePromise;
      closePromise = (async () => {
        quiescing = true;
        for (const response of sseResponses) response.end();
        if ('closeIdleConnections' in server) server.closeIdleConnections();
        const closed = new Promise<void>((resolve) => server.close(() => resolve()));
        const timeout = new Promise<'timeout'>((resolve) => setTimeout(() => resolve('timeout'), graceMs));
        const result = await Promise.race([closed.then(() => 'closed' as const), timeout]);
        if (result === 'timeout') {
          for (const socket of sockets) socket.destroy();
          await closed;
        }
        if (sockets.size > 0) {
          await Promise.all([...sockets].map((socket) => once(socket, 'close').then(() => undefined)));
        }
      })();
      return closePromise;
    },
  };
}
