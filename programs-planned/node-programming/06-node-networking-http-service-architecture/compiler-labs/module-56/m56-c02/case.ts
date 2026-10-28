import http from 'node:http';
export const agent = new http.Agent({ maxSockets: 'four' });
