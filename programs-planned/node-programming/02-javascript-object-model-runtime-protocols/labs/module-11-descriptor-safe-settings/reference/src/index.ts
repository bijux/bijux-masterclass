export type SettingValue = string | number | boolean;
export type Settings = Record<string, SettingValue> & { readonly summary: string };
export interface DescriptorReport {
  readonly key: string;
  readonly kind: 'data' | 'accessor';
  readonly enumerable: boolean;
  readonly configurable: boolean;
  readonly writable: boolean | null;
  readonly hasGetter: boolean;
  readonly hasSetter: boolean;
}

const SOURCE = Symbol('settings.source');
const FORBIDDEN = new Set(['__proto__', 'prototype', 'constructor']);

export function validateSettingKey(raw: string): string {
  const key = raw.trim();
  if (key === '' || FORBIDDEN.has(key)) throw new Error(`invalid setting key: ${raw}`);
  return key;
}

export function createSettings(values: Readonly<Record<string, SettingValue>>, source: string): Settings {
  const target = Object.create(null) as Record<PropertyKey, unknown>;
  for (const [rawKey, value] of Object.entries(values)) {
    const key = validateSettingKey(rawKey);
    Object.defineProperty(target, key, { value, writable: true, enumerable: true, configurable: true });
  }
  Object.defineProperty(target, SOURCE, { value: source, writable: false, enumerable: false, configurable: false });
  Object.defineProperty(target, 'summary', {
    get(this: Record<string, unknown>): string { return Object.keys(this).sort().join(', '); },
    enumerable: false,
    configurable: false,
  });
  return target as unknown as Settings;
}

export function settingsSource(settings: object): string {
  const value = Reflect.get(settings, SOURCE);
  if (typeof value !== 'string') throw new Error('settings source metadata is missing');
  return value;
}

export function describeOwnProperties(value: object): readonly DescriptorReport[] {
  return Reflect.ownKeys(value).map((key) => {
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (descriptor === undefined) throw new Error('own key disappeared during inspection');
    const data = 'value' in descriptor;
    return {
      key: typeof key === 'symbol' ? key.description === undefined ? 'Symbol()' : `Symbol(${key.description})` : key,
      kind: data ? 'data' : 'accessor',
      enumerable: descriptor.enumerable ?? false,
      configurable: descriptor.configurable ?? false,
      writable: data ? descriptor.writable ?? false : null,
      hasGetter: !data && descriptor.get !== undefined,
      hasSetter: !data && descriptor.set !== undefined,
    };
  });
}

export function snapshotSettings(settings: object): Readonly<Record<string, SettingValue>> {
  const result = Object.create(null) as Record<string, SettingValue>;
  for (const key of Object.keys(settings)) {
    const descriptor = Object.getOwnPropertyDescriptor(settings, key);
    if (descriptor === undefined) throw new Error(`property disappeared: ${key}`);
    if (!('value' in descriptor)) throw new Error(`enumerable accessor cannot be persisted: ${key}`);
    const value = descriptor.value;
    if (typeof value !== 'string' && typeof value !== 'number' && typeof value !== 'boolean') {
      throw new Error(`unsupported setting value: ${key}`);
    }
    result[key] = value;
  }
  return Object.freeze(result);
}
