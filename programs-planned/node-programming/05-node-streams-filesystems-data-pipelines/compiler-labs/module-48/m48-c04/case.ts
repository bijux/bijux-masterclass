import { spawn } from 'node:child_process';
import type { Readable } from 'node:stream';
const child = spawn(process.execPath, ['--version'], { stdio: 'ignore' });
const output: Readable = child.stdout;
void output;
