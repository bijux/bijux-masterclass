export function select<T, K extends keyof T>(value: T, key: K): T[K] { return value[key]; }
export type ValuesFor<T, K extends readonly (keyof T)[]> = { readonly [I in keyof K]: K[I] extends keyof T ? T[K[I]] : never };
export function valuesFor<T, const K extends readonly (keyof T)[]>(value: T, keys: K): ValuesFor<T, K> {
  return keys.map((key) => value[key]) as ValuesFor<T, K>;
}
export function project<T extends object, const K extends readonly (keyof T)[]>(value: T, keys: K): Pick<T, K[number]> {
  const output = {} as Pick<T, K[number]>;
  const seen = new Set<PropertyKey>();
  for (const key of keys) {
    if (seen.has(key)) throw new Error(`duplicate projection key: ${String(key)}`);
    seen.add(key);
    Object.defineProperty(output, key, { value: value[key], enumerable: true, writable: true, configurable: true });
  }
  return Object.freeze(output);
}
