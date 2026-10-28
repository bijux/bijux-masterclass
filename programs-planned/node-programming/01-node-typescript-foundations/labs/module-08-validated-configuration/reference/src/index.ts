export interface ProcessorConfig {
  readonly mode: 'scan' | 'rewrite';
  readonly concurrency: number;
  readonly maxInputBytes: number;
  readonly outputDirectory?: string;
  readonly logLevel: 'error' | 'warn' | 'info' | 'debug';
}
export interface ValidationIssue { readonly path: string; readonly message: string }
export type ValidationResult<T> = { readonly ok: true; readonly value: T } | { readonly ok: false; readonly issues: readonly ValidationIssue[] };

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
function positiveInteger(value: unknown, min: number, max: number): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value >= min && value <= max;
}

export function validateConfig(value: unknown): ValidationResult<ProcessorConfig> {
  if (!isRecord(value)) return { ok: false, issues: [{ path: '$', message: 'expected an object' }] };
  const issues: ValidationIssue[] = [];
  const allowed = new Set(['mode', 'concurrency', 'maxInputBytes', 'outputDirectory', 'logLevel']);
  for (const key of Object.keys(value).sort()) if (!allowed.has(key)) issues.push({ path: key, message: 'unknown property' });

  const mode = value['mode'];
  if (mode !== 'scan' && mode !== 'rewrite') issues.push({ path: 'mode', message: 'expected scan or rewrite' });
  const concurrency = value['concurrency'];
  if (!positiveInteger(concurrency, 1, 32)) issues.push({ path: 'concurrency', message: 'expected an integer from 1 to 32' });
  const maxInputBytes = value['maxInputBytes'];
  if (!positiveInteger(maxInputBytes, 1, 100_000_000)) issues.push({ path: 'maxInputBytes', message: 'expected an integer from 1 to 100000000' });
  const outputDirectory = value['outputDirectory'];
  if (mode === 'rewrite' && (typeof outputDirectory !== 'string' || outputDirectory.trim() === '')) {
    issues.push({ path: 'outputDirectory', message: 'required in rewrite mode' });
  } else if (outputDirectory !== undefined && (typeof outputDirectory !== 'string' || outputDirectory.trim() === '')) {
    issues.push({ path: 'outputDirectory', message: 'expected a nonempty string' });
  }
  const logLevel = value['logLevel'];
  if (logLevel !== 'error' && logLevel !== 'warn' && logLevel !== 'info' && logLevel !== 'debug') {
    issues.push({ path: 'logLevel', message: 'expected error, warn, info, or debug' });
  }
  if (issues.length > 0) return { ok: false, issues };

  if ((mode !== 'scan' && mode !== 'rewrite') || !positiveInteger(concurrency, 1, 32)
      || !positiveInteger(maxInputBytes, 1, 100_000_000)
      || (logLevel !== 'error' && logLevel !== 'warn' && logLevel !== 'info' && logLevel !== 'debug')) {
    throw new Error('validator invariant failed');
  }
  const base: Omit<ProcessorConfig, 'outputDirectory'> = { mode, concurrency, maxInputBytes, logLevel };
  return typeof outputDirectory === 'string'
    ? { ok: true, value: { ...base, outputDirectory: outputDirectory.trim() } }
    : { ok: true, value: base };
}

export function parseConfigJson(text: string): ValidationResult<ProcessorConfig> {
  let parsed: unknown;
  try { parsed = JSON.parse(text) as unknown; }
  catch (error: unknown) { throw new Error('configuration is not valid JSON', { cause: error }); }
  return validateConfig(parsed);
}
