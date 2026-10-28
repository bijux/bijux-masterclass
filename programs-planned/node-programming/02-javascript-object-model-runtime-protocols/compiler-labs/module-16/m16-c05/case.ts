const value = { [Symbol.toPrimitive](hint: string) { return hint === 'number' ? 4 : 'four'; } };
console.log(Number(value), String(value));
