export type SettingValue = string | number | boolean;

const FORBIDDEN = new Set(['__proto__', 'prototype', 'constructor']);

export function validateSettingKey(raw: string): string {
  const key = raw.trim();
  if (key === '' || FORBIDDEN.has(key)) throw new Error(`invalid setting key: ${raw}`);
  return key;
}

export function createPlainSettings(values: Readonly<Record<string, SettingValue>>): Record<string, SettingValue> {
  const result: Record<string, SettingValue> = {};
  for (const [rawKey, value] of Object.entries(values)) result[validateSettingKey(rawKey)] = value;
  return result;
}
