import { readFile } from 'node:fs/promises';
async function load(path: string): Promise<string> {
  return readFile(path, 'utf8');
}
console.log(typeof load);
