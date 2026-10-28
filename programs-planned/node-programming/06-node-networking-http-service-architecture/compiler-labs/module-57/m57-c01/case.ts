import type tls from 'node:tls';
export const options: tls.ConnectionOptions = { host:'127.0.0.1', servername:'localhost', rejectUnauthorized:true };
