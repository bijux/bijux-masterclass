import net from 'node:net';
export const server = net.createServer({ allowHalfOpen: 'yes' });
