const load = (id: string): number => id.length;
const render = (value: number): string => String(value);
const run = (id: string): string => render(load(id));
console.log(run('abc'));
