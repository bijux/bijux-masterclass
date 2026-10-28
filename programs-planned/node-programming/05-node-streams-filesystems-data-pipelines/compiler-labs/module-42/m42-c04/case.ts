import { Writable, type Readable } from 'node:stream';
const source: Readable = new Writable({ write(_chunk, _encoding, callback) { callback(); } });
void source;
