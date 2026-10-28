function* values() { try { yield 1; yield 2; } finally { console.log('closed'); } }
for (const value of values()) { console.log(value); break; }
