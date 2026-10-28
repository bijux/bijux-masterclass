import { PassThrough, type Duplex } from 'node:stream';
const channel: Duplex = new PassThrough();
void channel;
