import { Readable, type Writable } from 'node:stream';
const destination: Writable = Readable.from(['a']);
void destination;
