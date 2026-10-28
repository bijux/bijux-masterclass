import { readFile } from 'node:fs';
const result: Promise<string> = readFile('missing.txt', 'utf8', () => {});
console.log(result);
