import { StringDecoder } from 'node:string_decoder';
const bytes = Buffer.from('€');
const decoder = new StringDecoder('utf8');
console.log(decoder.write(bytes.subarray(0, 1)) + decoder.end(bytes.subarray(1)));
