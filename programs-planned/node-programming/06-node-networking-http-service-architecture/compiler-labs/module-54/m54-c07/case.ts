import http from 'node:http';
export const server = http.createServer((_request, response) => { response.writeHead(204); response.end(); });
