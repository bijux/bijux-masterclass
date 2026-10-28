import { gzip, gunzip } from 'node:zlib';
import { promisify } from 'node:util';
const packed = await promisify(gzip)(Buffer.from('hello'));
const plain = await promisify(gunzip)(packed);
console.log(plain.toString('utf8'));
