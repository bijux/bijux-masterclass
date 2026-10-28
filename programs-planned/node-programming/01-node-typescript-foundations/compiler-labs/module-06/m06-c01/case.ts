function get<T extends object, K extends keyof T>(value: T, key: K): T[K] {
  return value[key];
}
const item = { id: 1, title: 'Node' };
const title: string = get(item, 'title');
console.log(title);
