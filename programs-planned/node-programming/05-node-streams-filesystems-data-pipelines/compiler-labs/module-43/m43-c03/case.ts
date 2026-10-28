import { Readable, Writable } from 'node:stream';
import { pipeline } from 'node:stream/promises';
const done: Promise<void> = pipeline(Readable.from(['x']), new Writable({ write(_c, _e, cb) { cb(); } }));
void done;
