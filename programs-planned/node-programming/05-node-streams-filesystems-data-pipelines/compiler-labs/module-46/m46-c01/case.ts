import { StringDecoder } from 'node:string_decoder';
const decoder = new StringDecoder('utf8');
const text: string = decoder.write(Buffer.from('x'));
void text;
