import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
const dir = await mkdtemp(join(tmpdir(), 'course5-'));
try { const path = join(dir, 'value.txt'); await writeFile(path, 'ok'); console.log(await readFile(path, 'utf8')); } finally { await rm(dir, { recursive: true, force: true }); }
