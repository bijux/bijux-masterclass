import { PassThrough } from 'node:stream';
import type { FileHandle } from 'node:fs/promises';
const handle: FileHandle = new PassThrough();
void handle;
