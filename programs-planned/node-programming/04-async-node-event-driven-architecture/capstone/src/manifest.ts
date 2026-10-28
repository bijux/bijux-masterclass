import { readFile } from 'node:fs/promises';
import { ManifestError } from './errors.js';
import { TASK_HARBOR_VERSION, type Priority, type TaskManifest, type TaskSpec } from './domain.js';

const MAX_TASKS = 1_000;
const MAX_TEXT = 10_000;
const MAX_DEPENDENCIES = 100;
const MAX_TIMEOUT = 3_600_000;
const ID = /^[A-Za-z][A-Za-z0-9._-]{0,63}$/u;

type RecordValue = Record<string, unknown>;
function record(value: unknown, context: string): RecordValue {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) throw new ManifestError(`${context} must be an object`);
  return value as RecordValue;
}
function exact(value: RecordValue, allowed: readonly string[], context: string): void {
  const set = new Set(allowed);
  for (const key of Object.keys(value)) if (!set.has(key)) throw new ManifestError(`${context} has unknown field ${key}`);
}
function string(value: unknown, context: string, maximum = MAX_TEXT): string {
  if (typeof value !== 'string' || value.length === 0 || value.length > maximum) throw new ManifestError(`${context} must be a non-empty string of at most ${maximum} characters`);
  return value;
}
function integer(value: unknown, context: string, minimum: number, maximum: number): number {
  if (!Number.isInteger(value) || typeof value !== 'number' || value < minimum || value > maximum) {
    throw new ManifestError(`${context} must be an integer from ${minimum} to ${maximum}`);
  }
  return value;
}
function priority(value: unknown, context: string): Priority {
  if (value === undefined) return 'normal';
  if (value === 'low' || value === 'normal' || value === 'high') return value;
  throw new ManifestError(`${context} must be low, normal, or high`);
}
function dependencies(value: unknown, context: string): readonly string[] {
  if (value === undefined) return [];
  if (!Array.isArray(value) || value.length > MAX_DEPENDENCIES) throw new ManifestError(`${context} must be an array of at most ${MAX_DEPENDENCIES} IDs`);
  const output = value.map((item, index) => string(item, `${context}[${index}]`, 64));
  if (new Set(output).size !== output.length) throw new ManifestError(`${context} contains a duplicate`);
  return output;
}

function task(value: unknown, index: number): TaskSpec {
  const context = `tasks[${index}]`;
  const input = record(value, context);
  const kind = string(input.kind, `${context}.kind`, 32);
  const common = {
    id: string(input.id, `${context}.id`, 64),
    dependsOn: dependencies(input.dependsOn, `${context}.dependsOn`),
    priority: priority(input.priority, `${context}.priority`),
  };
  if (!ID.test(common.id)) throw new ManifestError(`${context}.id has invalid syntax`);
  const timeoutMs = input.timeoutMs === undefined ? undefined : integer(input.timeoutMs, `${context}.timeoutMs`, 1, MAX_TIMEOUT);
  if (kind === 'delay') {
    exact(input, ['id', 'kind', 'milliseconds', 'dependsOn', 'priority', 'timeoutMs'], context);
    const base = { ...common, kind, milliseconds: integer(input.milliseconds, `${context}.milliseconds`, 0, MAX_TIMEOUT) } as const;
    return timeoutMs === undefined ? base : { ...base, timeoutMs };
  }
  if (kind === 'echo' || kind === 'uppercase') {
    exact(input, ['id', 'kind', 'text', 'dependsOn', 'priority', 'timeoutMs'], context);
    const base = { ...common, kind, text: string(input.text, `${context}.text`) } as const;
    return timeoutMs === undefined ? base : { ...base, timeoutMs };
  }
  if (kind === 'fail') {
    exact(input, ['id', 'kind', 'message', 'dependsOn', 'priority', 'timeoutMs'], context);
    const base = { ...common, kind, message: string(input.message, `${context}.message`) } as const;
    return timeoutMs === undefined ? base : { ...base, timeoutMs };
  }
  throw new ManifestError(`${context}.kind is unsupported: ${kind}`);
}

export function parseManifest(value: unknown): TaskManifest {
  const input = record(value, 'manifest');
  exact(input, ['version', 'tasks'], 'manifest');
  if (input.version !== TASK_HARBOR_VERSION) throw new ManifestError(`manifest.version must be ${TASK_HARBOR_VERSION}`);
  if (!Array.isArray(input.tasks) || input.tasks.length === 0 || input.tasks.length > MAX_TASKS) {
    throw new ManifestError(`manifest.tasks must contain 1 to ${MAX_TASKS} tasks`);
  }
  return Object.freeze({ version: TASK_HARBOR_VERSION, tasks: Object.freeze(input.tasks.map(task)) });
}

export function parseManifestText(text: string): TaskManifest {
  let value: unknown;
  try { value = JSON.parse(text); } catch (error) { throw new ManifestError(`invalid JSON: ${error instanceof Error ? error.message : String(error)}`); }
  return parseManifest(value);
}

export async function loadManifest(path: string): Promise<TaskManifest> {
  return parseManifestText(await readFile(path, 'utf8'));
}
