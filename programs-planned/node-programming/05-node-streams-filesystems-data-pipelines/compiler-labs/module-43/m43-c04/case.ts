import { Readable } from 'node:stream';
import { pipeline } from 'node:stream/promises';
const done = pipeline(Readable.from(['x']), 42);
void done;
