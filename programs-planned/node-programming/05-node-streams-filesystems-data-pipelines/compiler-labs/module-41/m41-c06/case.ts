import { Buffer } from 'node:buffer';
const backing = Buffer.from([1, 2]);
const copy = Buffer.from(backing.subarray(0, 1));
backing[0] = 9;
console.log(copy[0]);
