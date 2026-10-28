import { gunzip } from 'node:zlib';
import { promisify } from 'node:util';
await promisify(gunzip)(Buffer.from('not-gzip'));
