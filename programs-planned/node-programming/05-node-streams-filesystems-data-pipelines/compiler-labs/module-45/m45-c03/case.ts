import type { FileHandle } from 'node:fs/promises';
async function sync(handle: FileHandle): Promise<void> { await handle.sync(); }
void sync;
