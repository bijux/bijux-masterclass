import { PassThrough } from 'node:stream';
const a = new PassThrough(); const b = new PassThrough();
let left = 0; let right = 0;
a.on('data', chunk => { left += Buffer.from(chunk).length; });
b.on('data', chunk => { right += Buffer.from(chunk).length; });
a.end('abc'); b.end('abc');
await Promise.all([new Promise<void>(resolve => a.on('end', resolve)), new Promise<void>(resolve => b.on('end', resolve))]);
console.log(`${left}:${right}`);
