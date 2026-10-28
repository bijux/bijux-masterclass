import { PassThrough, type Duplex } from 'node:stream';
const branch: Duplex = new PassThrough();
void branch;
