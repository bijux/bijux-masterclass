import { createReadStream, createWriteStream } from 'node:fs';
const source = createReadStream('in.txt');
const sink = createWriteStream('out.txt');
void source; void sink;
