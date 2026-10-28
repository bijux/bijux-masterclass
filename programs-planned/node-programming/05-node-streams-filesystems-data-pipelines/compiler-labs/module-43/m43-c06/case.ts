import { Writable } from 'node:stream';
import { finished } from 'node:stream/promises';
const sink = new Writable({ write(_c, _e, cb) { cb(); } });
const result: Promise<string> = finished(sink);
void result;
