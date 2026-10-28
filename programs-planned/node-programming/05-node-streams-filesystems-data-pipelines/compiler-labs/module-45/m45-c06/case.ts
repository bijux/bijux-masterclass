import { createWriteStream, type ReadStream } from 'node:fs';
const source: ReadStream = createWriteStream('out.txt');
void source;
