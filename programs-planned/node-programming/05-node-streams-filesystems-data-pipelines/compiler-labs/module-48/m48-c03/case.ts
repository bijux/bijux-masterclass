import { spawn } from 'node:child_process';
const child = spawn(process.execPath, ['--version'], { stdio: ['ignore', 'pipe', 'pipe'] });
if (child.stdout) child.stdout.resume();
