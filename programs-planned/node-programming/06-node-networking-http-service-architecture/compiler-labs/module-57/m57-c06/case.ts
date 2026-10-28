import type tls from 'node:tls';
export function protocol(socket: tls.TLSSocket): string { const value: string = socket.alpnProtocol; return value; }
