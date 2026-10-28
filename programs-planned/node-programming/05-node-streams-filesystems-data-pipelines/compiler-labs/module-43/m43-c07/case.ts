import { Writable } from 'node:stream';
const sink = new Writable({ highWaterMark: 1, write(_c, _e, cb) { setImmediate(cb); } });
console.log(sink.write(Buffer.from('xx')));
sink.end();
