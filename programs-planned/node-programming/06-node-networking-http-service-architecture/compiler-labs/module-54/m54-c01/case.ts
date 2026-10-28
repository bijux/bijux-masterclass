import type http from 'node:http';
export function first(headers: http.IncomingHttpHeaders, name: string): string | undefined { const value = headers[name]; return Array.isArray(value) ? value[0] : value; }
