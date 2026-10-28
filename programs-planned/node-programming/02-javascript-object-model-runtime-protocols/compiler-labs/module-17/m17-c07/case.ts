const iterator: Iterator<number> = { next: () => ({ done: true, value: undefined }) };
for (const value of iterator) console.log(value);
