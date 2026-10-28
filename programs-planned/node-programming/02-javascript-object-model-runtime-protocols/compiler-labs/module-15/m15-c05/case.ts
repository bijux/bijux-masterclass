const calls: string[] = [];
const store = { load() { calls.push('load'); return 'x'; } };
const render = { format(value: string) { calls.push('render'); return value.toUpperCase(); } };
console.log(render.format(store.load()), calls.join(','));
