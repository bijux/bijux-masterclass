import { readFile, type FileHandle } from 'node:fs/promises';
const handle: Promise<FileHandle> = readFile('example.txt');
void handle;
