import http from 'node:http';
import { randomUUID } from 'node:crypto';

export class HttpBoundaryError extends Error {
  constructor(
    readonly code: 'BODY_TOO_LARGE' | 'BODY_REQUIRED' | 'UNSUPPORTED_MEDIA_TYPE' | 'MALFORMED_JSON' | 'INVALID_BODY',
    readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = 'HttpBoundaryError';
  }
}

export async function readBoundedBody(
  request: http.IncomingMessage,
  maxBytes: number,
): Promise<Buffer> {
  if (!Number.isInteger(maxBytes) || maxBytes < 0) throw new RangeError('maxBytes');
  const declared = request.headers['content-length'];
  if (typeof declared === 'string') {
    const length = Number(declared);
    if (Number.isInteger(length) && length > maxBytes) {
      throw new HttpBoundaryError('BODY_TOO_LARGE', 413, `body exceeds ${maxBytes} bytes`);
    }
  }
  const chunks: Buffer[] = [];
  let total = 0;
  for await (const chunk of request) {
    const bytes = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    total += bytes.byteLength;
    if (total > maxBytes) {
      throw new HttpBoundaryError('BODY_TOO_LARGE', 413, `body exceeds ${maxBytes} bytes`);
    }
    chunks.push(bytes);
  }
  return Buffer.concat(chunks, total);
}

function contentType(value: string | undefined): string | undefined {
  return value?.split(';', 1)[0]?.trim().toLowerCase();
}

export async function parseJsonObject(
  request: http.IncomingMessage,
  maxBytes: number,
): Promise<Record<string, unknown>> {
  if (contentType(request.headers['content-type']) !== 'application/json') {
    throw new HttpBoundaryError('UNSUPPORTED_MEDIA_TYPE', 415, 'application/json is required');
  }
  const bytes = await readBoundedBody(request, maxBytes);
  if (bytes.byteLength === 0) throw new HttpBoundaryError('BODY_REQUIRED', 400, 'body is required');
  let value: unknown;
  try {
    value = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes));
  } catch {
    throw new HttpBoundaryError('MALFORMED_JSON', 400, 'body is not valid JSON');
  }
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new HttpBoundaryError('INVALID_BODY', 422, 'a JSON object is required');
  }
  return value as Record<string, unknown>;
}

function problem(error: HttpBoundaryError, requestId: string): Buffer {
  return Buffer.from(JSON.stringify({
    type: `https://strict-http.invalid/problems/${error.code.toLowerCase().replaceAll('_', '-')}`,
    title: error.message,
    status: error.status,
    code: error.code,
    detail: error.message.slice(0, 200),
    requestId,
  }), 'utf8');
}

function finiteJson(
  response: http.ServerResponse,
  status: number,
  value: unknown,
  head: boolean,
  headers: Readonly<Record<string, string>> = {},
): void {
  const body = Buffer.from(JSON.stringify(value), 'utf8');
  response.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'content-length': String(body.byteLength),
    ...headers,
  });
  response.end(head ? undefined : body);
}

export async function startStrictServer(options: {
  readonly maxBodyBytes: number;
  readonly maxConnections: number;
}): Promise<{
  readonly url: string;
  readonly calls: () => number;
  readonly activeRequests: () => number;
  readonly activeSockets: () => number;
  quiesce(): void;
  close(graceMs?: number): Promise<void>;
}> {
  let calls = 0;
  let activeRequests = 0;
  let quiescing = false;
  const sockets = new Set<import('node:net').Socket>();

  const server = http.createServer(async (request, response) => {
    activeRequests += 1;
    const requestIdHeader = request.headers['x-request-id'];
    const requestId = typeof requestIdHeader === 'string' && /^[A-Za-z0-9._-]{1,64}$/.test(requestIdHeader)
      ? requestIdHeader
      : randomUUID();
    response.setHeader('x-request-id', requestId);
    try {
      if (quiescing) {
        const body = problem(new HttpBoundaryError('INVALID_BODY', 503, 'server is quiescing'), requestId);
        response.writeHead(503, {
          'content-type': 'application/problem+json',
          'content-length': String(body.byteLength),
        });
        response.end(body);
        return;
      }
      const url = new URL(request.url ?? '/', 'http://server.invalid');
      const method = request.method ?? '';
      if (url.pathname === '/health') {
        if (method !== 'GET' && method !== 'HEAD') {
          response.writeHead(405, { allow: 'GET, HEAD', 'content-length': '0' });
          response.end();
          return;
        }
        finiteJson(response, 200, { ok: true }, method === 'HEAD');
        return;
      }
      if (url.pathname === '/echo') {
        if (method !== 'POST') {
          response.writeHead(405, { allow: 'POST', 'content-length': '0' });
          response.end();
          return;
        }
        const value = await parseJsonObject(request, options.maxBodyBytes);
        calls += 1;
        finiteJson(response, 200, { value }, false);
        return;
      }
      response.writeHead(404, { 'content-length': '0' });
      response.end();
    } catch (error) {
      const boundary = error instanceof HttpBoundaryError
        ? error
        : new HttpBoundaryError('INVALID_BODY', 500, 'internal error');
      if (!response.headersSent) {
        const body = problem(boundary, requestId);
        response.writeHead(boundary.status, {
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
  });
  server.maxConnections = options.maxConnections;
  server.headersTimeout = 2_000;
  server.requestTimeout = 2_000;
  server.keepAliveTimeout = 500;
  server.on('connection', (socket) => {
    sockets.add(socket);
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
    url: `http://127.0.0.1:${observed.port}`,
    calls: () => calls,
    activeRequests: () => activeRequests,
    activeSockets: () => sockets.size,
    quiesce: () => { quiescing = true; },
    close: async (graceMs = 100) => {
      quiescing = true;
      await new Promise<void>((resolve) => server.close(() => resolve()));
      const deadline = Date.now() + graceMs;
      while ((activeRequests > 0 || sockets.size > 0) && Date.now() < deadline) {
        await new Promise((resolve) => setTimeout(resolve, 5));
      }
      for (const socket of sockets) socket.destroy();
    },
  };
}
