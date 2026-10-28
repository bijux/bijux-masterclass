const base = {};
Object.defineProperty(base, 'label', { get(this: { name: string }): string { return this.name; } });
const child = Object.create(base) as { name: string; label: string };
child.name = 'child';
console.log(child.label);
