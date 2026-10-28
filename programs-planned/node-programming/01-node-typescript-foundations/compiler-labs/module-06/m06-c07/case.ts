const groups = new Map<string, number[]>([['b', [2]], ['a', [1]]]);
const rendered = [...groups.keys()].sort().map((key) => `${key}:${groups.get(key)?.join(',') ?? ''}`);
console.log(rendered.join('|'));
