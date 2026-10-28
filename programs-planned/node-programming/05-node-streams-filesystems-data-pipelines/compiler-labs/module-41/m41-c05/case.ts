import { Buffer } from 'node:buffer';
const backing = Buffer.from([1, 2]);
const view = backing.subarray(0, 1);
backing[0] = 9;
console.log(view[0]);
