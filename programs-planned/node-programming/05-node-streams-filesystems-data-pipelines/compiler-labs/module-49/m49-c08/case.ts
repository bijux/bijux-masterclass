import { Writable } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { Readable } from 'node:stream';
const sink = new Writable({ write(_c, _e, callback) { callback(new Error('branch failed')); } });
await pipeline(Readable.from(['x']), sink);
