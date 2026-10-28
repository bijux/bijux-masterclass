import { open, type FileHandle } from 'node:fs/promises';
const handle: Promise<FileHandle> = open('example.txt', 'r');
void handle;
