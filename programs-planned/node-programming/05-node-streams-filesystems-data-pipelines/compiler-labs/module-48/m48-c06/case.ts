import { spawn } from 'node:child_process';
spawn(process.execPath, [], { stdio: 'telepathy' });
