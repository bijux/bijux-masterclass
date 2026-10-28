import { Readable } from 'node:stream';
let count = 0;
for await (const _chunk of Readable.from(['a', 'b'])) count += 1;
console.log(count);
