import { Readable, Writable } from 'node:stream';
const source = Readable.from(['a']);
const sink = new Writable({ write(_chunk, _encoding, callback) { callback(); } });
void source; void sink;
