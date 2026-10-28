const text = 'not an absolute endpoint';
try { new URL(text); } catch { throw new Error('invalid endpoint'); }
