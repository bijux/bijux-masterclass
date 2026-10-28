import { Readable } from 'node:stream';
let out = '';
for await (const chunk of Readable.from(['a', 'b'])) out += String(chunk);
console.log(out);
