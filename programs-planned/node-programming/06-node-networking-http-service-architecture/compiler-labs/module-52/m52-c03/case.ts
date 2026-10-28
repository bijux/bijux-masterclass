import type net from 'node:net';
export function closeSocket(socket: net.Socket): void { socket.end(); }
