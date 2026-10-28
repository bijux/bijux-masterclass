import { spawn } from 'node:child_process';
import { once } from 'node:events';
const child = spawn(process.execPath, ['-e', "process.stdout.write(process.argv[1])", 'a b'], { stdio: ['ignore', 'pipe', 'inherit'] });
let output = '';
child.stdout?.setEncoding('utf8');
child.stdout?.on('data', chunk => { output += String(chunk); });
await once(child, 'close');
console.log(output);
