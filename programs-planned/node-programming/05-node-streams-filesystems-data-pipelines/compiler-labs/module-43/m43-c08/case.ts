import { Writable } from 'node:stream';
const sink = new Writable({ highWaterMark: 1, write(_c, _e, cb) { setImmediate(cb); } });
if (!sink.write(Buffer.from('xx'))) throw new Error('backpressure ignored');
