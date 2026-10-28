import { Writable } from 'node:stream';
const sink = new Writable({ write(_chunk, _encoding, callback) { callback(); } });
const accepted: boolean = sink.write('x');
void accepted;
