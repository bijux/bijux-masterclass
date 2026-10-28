import { Writable } from 'node:stream';
const sink = new Writable({ write(_chunk, _encoding, callback) { callback(); } });
const bytes: number = sink.write('x');
void bytes;
