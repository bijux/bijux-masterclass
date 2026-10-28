import { Buffer } from 'node:buffer';
const backing = Buffer.from([9, 1, 2, 8]);
const copy = Buffer.from(backing.subarray(1, 3));
void copy;
