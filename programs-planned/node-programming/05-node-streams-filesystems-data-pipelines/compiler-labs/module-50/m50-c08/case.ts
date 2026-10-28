const limit = 4; const line = '12345';
if (Buffer.byteLength(line) > limit) throw new Error('line exceeds limit');
