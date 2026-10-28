interface RecordValue { name: string; values: number[] }
const source: RecordValue = { name: 'x', values: [1] };
const copy: RecordValue = structuredClone(source);
console.log(copy.name);
