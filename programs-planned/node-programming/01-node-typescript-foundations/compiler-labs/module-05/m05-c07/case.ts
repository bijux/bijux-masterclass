type Level = 'info' | 'warn' | 'error';
const raw: string = process.argv[2] ?? 'info';
const level: Level = raw;
console.log(level);
