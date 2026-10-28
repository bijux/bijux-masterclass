import http from 'node:http';
export const agent = new http.Agent({ keepAlive: true, maxSockets: 4 });
