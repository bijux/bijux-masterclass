const pending = Buffer.from([0, 0]);
if (pending.byteLength !== 0) throw new Error('truncated frame prefix');
