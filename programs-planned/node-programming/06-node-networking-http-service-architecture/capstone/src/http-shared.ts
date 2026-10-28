import { randomUUID } from 'node:crypto';
import {
  parseIdempotencyKey,
  parseJobId,
  validateSubmitCommand,
} from './domain.js';
import { ServiceProblem, toProblem } from './errors.js';
import type { ServiceWireApplication } from './service.js';
import type { ServiceEvent } from './events.js';

export interface FiniteHttpRequest {
  readonly method: string;
  readonly url: URL;
  readonly headers: ReadonlyMap<string, string | readonly string[]>;
  readonly body: Buffer;
  readonly requestId: string;
}

export interface FiniteHttpResponse {
  readonly status: number;
  readonly headers: Readonly<Record<string, string>>;
  readonly body: Buffer;
  readonly omitBody: boolean;
}

export function requestIdFromHeaders(
  headers: ReadonlyMap<string, string | readonly string[]>,
): string {
  const value = headers.get('x-request-id');
  if (typeof value === 'string' && /^[A-Za-z0-9._:-]{1,64}$/.test(value)) return value;
  return randomUUID();
}

function jsonResponse(
  status: number,
  value: unknown,
  options: {
    readonly omitBody?: boolean;
    readonly headers?: Readonly<Record<string, string>>;
    readonly contentType?: string;
  } = {},
): FiniteHttpResponse {
  const body = Buffer.from(JSON.stringify(value), 'utf8');
  return {
    status,
    headers: {
      'content-type': options.contentType ?? 'application/json; charset=utf-8',
      'content-length': String(body.byteLength),
      ...options.headers,
    },
    body,
    omitBody: options.omitBody ?? false,
  };
}

function emptyResponse(status: number, headers: Readonly<Record<string, string>> = {}): FiniteHttpResponse {
  return {
    status,
    headers: { 'content-length': '0', ...headers },
    body: Buffer.alloc(0),
    omitBody: true,
  };
}

function header(
  headers: ReadonlyMap<string, string | readonly string[]>,
  name: string,
): string | undefined {
  const value = headers.get(name);
  return typeof value === 'string' ? value : value?.[0];
}

function parseJsonObject(request: FiniteHttpRequest): unknown {
  const media = header(request.headers, 'content-type')?.split(';', 1)[0]?.trim().toLowerCase();
  if (media !== 'application/json') {
    throw new ServiceProblem('UNSUPPORTED_MEDIA_TYPE', 415, 'Content-Type application/json is required');
  }
  if (request.body.byteLength === 0) {
    throw new ServiceProblem('BODY_REQUIRED', 400, 'Request body is required');
  }
  try {
    return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(request.body)) as unknown;
  } catch {
    throw new ServiceProblem('MALFORMED_JSON', 400, 'Request body is not valid UTF-8 JSON');
  }
}

function problemResponse(error: unknown, requestId: string): FiniteHttpResponse {
  const problem = toProblem(error, requestId);
  return jsonResponse(problem.status, problem, {
    contentType: 'application/problem+json',
  });
}

function route(method: string, pathname: string):
  | { readonly kind: 'health'; readonly head: boolean }
  | { readonly kind: 'stats' }
  | { readonly kind: 'submit' }
  | { readonly kind: 'job'; readonly id: string; readonly head: boolean }
  | { readonly kind: 'method'; readonly allow: string }
  | { readonly kind: 'not-found' } {
  if (pathname === '/v1/health') {
    if (method === 'GET' || method === 'HEAD') return { kind: 'health', head: method === 'HEAD' };
    return { kind: 'method', allow: 'GET, HEAD' };
  }
  if (pathname === '/v1/stats') {
    if (method === 'GET') return { kind: 'stats' };
    return { kind: 'method', allow: 'GET' };
  }
  if (pathname === '/v1/jobs') {
    if (method === 'POST') return { kind: 'submit' };
    return { kind: 'method', allow: 'POST' };
  }
  const segments = pathname.split('/');
  if (segments.length === 4 && segments[1] === 'v1' && segments[2] === 'jobs' && segments[3]) {
    if (method === 'GET' || method === 'HEAD') {
      return { kind: 'job', id: segments[3], head: method === 'HEAD' };
    }
    return { kind: 'method', allow: 'GET, HEAD' };
  }
  return { kind: 'not-found' };
}

export function dispatchFinite(
  application: ServiceWireApplication,
  request: FiniteHttpRequest,
): FiniteHttpResponse {
  try {
    const matched = route(request.method, request.url.pathname);
    switch (matched.kind) {
      case 'not-found':
        throw new ServiceProblem('ROUTE_NOT_FOUND', 404, 'Route does not exist');
      case 'method': {
        const response = problemResponse(
          new ServiceProblem('METHOD_NOT_ALLOWED', 405, 'Method is not allowed for this route'),
          request.requestId,
        );
        return { ...response, headers: { ...response.headers, allow: matched.allow } };
      }
      case 'health': {
        const stats = application.stats();
        return jsonResponse(200, {
          health: stats.health,
          readiness: stats.readiness,
          state: stats.state,
        }, { omitBody: matched.head });
      }
      case 'stats':
        return jsonResponse(200, application.stats());
      case 'submit': {
        const key = parseIdempotencyKey(header(request.headers, 'idempotency-key'));
        const command = validateSubmitCommand(parseJsonObject(request));
        const result = application.submit(command, key);
        return jsonResponse(202, { ...result.job, replay: result.replay }, {
          headers: {
            location: `/v1/jobs/${result.job.id}`,
            etag: result.etag,
          },
        });
      }
      case 'job': {
        const id = parseJobId(matched.id);
        const found = application.getJob(id);
        if (!found) throw new ServiceProblem('JOB_NOT_FOUND', 404, 'Job does not exist');
        const condition = header(request.headers, 'if-none-match');
        if (condition === found.etag) {
          return emptyResponse(304, { etag: found.etag });
        }
        return jsonResponse(200, found.job, {
          omitBody: matched.head,
          headers: { etag: found.etag },
        });
      }
    }
  } catch (error) {
    return problemResponse(error, request.requestId);
  }
}

export function encodeSseEvent(event: ServiceEvent): Buffer {
  const { sequence, type, ...data } = event;
  const json = JSON.stringify(data);
  const lines = json.split(/\r?\n/).map((line) => `data: ${line}`).join('\n');
  return Buffer.from(`id: ${sequence}\nevent: ${type}\n${lines}\n\n`, 'utf8');
}
