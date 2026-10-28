const values = await Promise.all([Promise.resolve(1), Promise.resolve('node')] as const);
const count: number = values[0];
const label: string = values[1];
console.log(count, label);
