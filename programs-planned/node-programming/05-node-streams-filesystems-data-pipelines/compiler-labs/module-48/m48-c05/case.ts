import { spawn } from 'node:child_process';
const child = spawn(process.execPath, ['--version']);
const code: number | null = child.exitCode;
void code;
