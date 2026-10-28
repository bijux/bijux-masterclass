import { Transform } from 'node:stream';
const upper = new Transform({ transform(chunk, _encoding, callback) { callback(null, Buffer.from(chunk).toString('utf8').toUpperCase()); } });
void upper;
