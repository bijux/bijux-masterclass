import type http2 from 'node:http2';
export const settings: http2.Settings = { maxConcurrentStreams: 16 };
