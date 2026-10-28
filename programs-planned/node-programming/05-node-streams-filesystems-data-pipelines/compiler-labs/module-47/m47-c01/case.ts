import { createGzip } from 'node:zlib';
import type { Transform } from 'node:stream';
const gzip: Transform = createGzip();
void gzip;
