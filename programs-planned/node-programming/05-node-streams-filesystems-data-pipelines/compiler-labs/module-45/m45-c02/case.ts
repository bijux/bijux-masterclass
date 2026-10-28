import { readFile } from 'node:fs/promises';
const bytes: Buffer = readFile('example.txt');
void bytes;
