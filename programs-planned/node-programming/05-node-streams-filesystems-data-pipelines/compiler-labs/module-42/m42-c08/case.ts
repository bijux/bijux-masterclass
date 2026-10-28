import { Writable } from 'node:stream';
const sink = new Writable({ write(_chunk, _encoding, callback) { callback(); } });
sink.end();
if (sink.writableEnded) throw new Error('write after end rejected');
