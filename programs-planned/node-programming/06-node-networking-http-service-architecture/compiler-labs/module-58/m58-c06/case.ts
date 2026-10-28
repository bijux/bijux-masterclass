import http2 from 'node:http2';
export const session = http2.connect(42);
