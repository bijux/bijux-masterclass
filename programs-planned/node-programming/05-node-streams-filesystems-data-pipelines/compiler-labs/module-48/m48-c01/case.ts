import { spawn } from 'node:child_process';
const child = spawn(process.execPath, ['--version'], { shell: false });
void child;
