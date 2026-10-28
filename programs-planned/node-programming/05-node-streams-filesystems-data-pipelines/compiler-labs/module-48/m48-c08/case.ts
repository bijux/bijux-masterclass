import { spawn } from 'node:child_process';
import { once } from 'node:events';
const child = spawn('/definitely-not-present-course5-program', []);
await once(child, 'error');
throw new Error('ENOENT spawn failure');
