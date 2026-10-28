import { once } from 'node:events';
import { Writable } from 'node:stream';
const sink = new Writable({ write(_c, _e, cb) { cb(); } });
const controller = new AbortController();
const wait: Promise<unknown[]> = once(sink, 'drain', { signal: controller.signal });
void wait;
