import { spawn } from 'node:child_process';
const child = spawn(process.execPath, '--version');
void child;
