import { calibrationFor } from './internal.js';

export interface Reading { readonly celsius: number; readonly profile: string }

export function calibratedCelsius(raw: number, profile: string): Reading {
  if (!Number.isFinite(raw)) throw new Error('temperature must be finite');
  return { celsius: raw + calibrationFor(profile), profile };
}

export function toFahrenheit(reading: Reading): number {
  return reading.celsius * 9 / 5 + 32;
}
