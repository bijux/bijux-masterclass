import type http2 from 'node:http2';
export function method(headers:http2.IncomingHttpHeaders): string | undefined { const value=headers[':method']; return typeof value === 'string' ? value : undefined; }
