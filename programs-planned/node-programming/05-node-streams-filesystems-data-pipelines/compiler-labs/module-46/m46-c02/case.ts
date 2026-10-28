import { StringDecoder } from 'node:string_decoder';
const decoder = new StringDecoder('utf8');
decoder.write(42);
