import {
  normalizeTimestamp,
  normalizeTopic,
  validateActualMinutes,
  validatePlannedMinutes,
  validateSessionId,
  type StudyLedger,
  type StudySession,
} from './domain.js';
import { DomainError, StorageValidationError, type ValidationIssue } from './errors.js';

const FORMAT = 'STUDY_LEDGER_V1';
const ROOT_KEYS = new Set(['format', 'nextId', 'sessions']);
const BASE_KEYS = ['id', 'status', 'topic', 'plannedMinutes', 'createdAt'] as const;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function addUnknownKeyIssues(
  value: Record<string, unknown>,
  allowed: ReadonlySet<string>,
  path: string,
  issues: ValidationIssue[],
): void {
  for (const key of Object.keys(value).sort()) {
    if (!allowed.has(key)) issues.push({ path: `${path}.${key}`, message: 'unknown property' });
  }
}

function collect<T>(
  path: string,
  issues: ValidationIssue[],
  operation: () => T,
): T | undefined {
  try {
    return operation();
  } catch (error: unknown) {
    issues.push({ path, message: error instanceof Error ? error.message : 'invalid value' });
    return undefined;
  }
}

function requiredString(
  value: Record<string, unknown>,
  key: string,
  path: string,
  issues: ValidationIssue[],
): string | undefined {
  const candidate = value[key];
  if (typeof candidate !== 'string') {
    issues.push({ path: `${path}.${key}`, message: 'expected a string' });
    return undefined;
  }
  return candidate;
}

function requiredNumber(
  value: Record<string, unknown>,
  key: string,
  path: string,
  issues: ValidationIssue[],
): number | undefined {
  const candidate = value[key];
  if (typeof candidate !== 'number') {
    issues.push({ path: `${path}.${key}`, message: 'expected a number' });
    return undefined;
  }
  return candidate;
}

function sessionKeys(status: string): ReadonlySet<string> {
  const keys = new Set<string>(BASE_KEYS);
  if (status === 'active') keys.add('startedAt');
  if (status === 'completed') {
    keys.add('startedAt');
    keys.add('completedAt');
    keys.add('actualMinutes');
    keys.add('note');
  }
  if (status === 'abandoned') {
    keys.add('startedAt');
    keys.add('abandonedAt');
    keys.add('reason');
  }
  return keys;
}

function decodeSession(raw: unknown, index: number, issues: ValidationIssue[]): StudySession | undefined {
  const path = `$.sessions[${index}]`;
  if (!isRecord(raw)) {
    issues.push({ path, message: 'expected an object' });
    return undefined;
  }
  const status = requiredString(raw, 'status', path, issues);
  if (status !== undefined) addUnknownKeyIssues(raw, sessionKeys(status), path, issues);
  const rawId = requiredNumber(raw, 'id', path, issues);
  const rawTopic = requiredString(raw, 'topic', path, issues);
  const rawPlannedMinutes = requiredNumber(raw, 'plannedMinutes', path, issues);
  const rawCreatedAt = requiredString(raw, 'createdAt', path, issues);

  const id = rawId === undefined ? undefined : collect(`${path}.id`, issues, () => validateSessionId(rawId));
  const topic = rawTopic === undefined ? undefined : collect(`${path}.topic`, issues, () => normalizeTopic(rawTopic));
  const plannedMinutes = rawPlannedMinutes === undefined
    ? undefined
    : collect(`${path}.plannedMinutes`, issues, () => validatePlannedMinutes(rawPlannedMinutes));
  const createdAt = rawCreatedAt === undefined
    ? undefined
    : collect(`${path}.createdAt`, issues, () => normalizeTimestamp(rawCreatedAt, 'createdAt'));

  if (id === undefined || topic === undefined || plannedMinutes === undefined || createdAt === undefined || status === undefined) {
    return undefined;
  }

  try {
    switch (status) {
      case 'planned':
        return { id, status, topic, plannedMinutes, createdAt };
      case 'active': {
        const startedAtRaw = requiredString(raw, 'startedAt', path, issues);
        if (startedAtRaw === undefined) return undefined;
        const startedAt = normalizeTimestamp(startedAtRaw, 'startedAt');
        if (Date.parse(startedAt) < Date.parse(createdAt)) throw new DomainError('DOMAIN_INVALID', 'startedAt precedes createdAt');
        return { id, status, topic, plannedMinutes, createdAt, startedAt };
      }
      case 'completed': {
        const startedAtRaw = requiredString(raw, 'startedAt', path, issues);
        const completedAtRaw = requiredString(raw, 'completedAt', path, issues);
        const actualRaw = requiredNumber(raw, 'actualMinutes', path, issues);
        const noteRaw = raw['note'];
        if (startedAtRaw === undefined || completedAtRaw === undefined || actualRaw === undefined) return undefined;
        if (noteRaw !== null && typeof noteRaw !== 'string') {
          issues.push({ path: `${path}.note`, message: 'expected a string or null' });
          return undefined;
        }
        const startedAt = normalizeTimestamp(startedAtRaw, 'startedAt');
        const completedAt = normalizeTimestamp(completedAtRaw, 'completedAt');
        const actualMinutes = validateActualMinutes(actualRaw);
        if (Date.parse(startedAt) < Date.parse(createdAt)) throw new DomainError('DOMAIN_INVALID', 'startedAt precedes createdAt');
        if (Date.parse(completedAt) < Date.parse(startedAt)) throw new DomainError('DOMAIN_INVALID', 'completedAt precedes startedAt');
        const note = noteRaw === null ? null : noteRaw.trim();
        if (note !== null && /[\u0000-\u001f\u007f]/u.test(note)) throw new DomainError('DOMAIN_INVALID', 'note contains control characters');
        if (note !== null && note.length > 2_000) throw new DomainError('DOMAIN_INVALID', 'note is too long');
        return { id, status, topic, plannedMinutes, createdAt, startedAt, completedAt, actualMinutes, note };
      }
      case 'abandoned': {
        const startedAtRaw = raw['startedAt'];
        const abandonedAtRaw = requiredString(raw, 'abandonedAt', path, issues);
        const reasonRaw = requiredString(raw, 'reason', path, issues);
        if ((startedAtRaw !== null && typeof startedAtRaw !== 'string') || abandonedAtRaw === undefined || reasonRaw === undefined) {
          if (startedAtRaw !== null && typeof startedAtRaw !== 'string') {
            issues.push({ path: `${path}.startedAt`, message: 'expected a string or null' });
          }
          return undefined;
        }
        const startedAt = startedAtRaw === null ? null : normalizeTimestamp(startedAtRaw, 'startedAt');
        const abandonedAt = normalizeTimestamp(abandonedAtRaw, 'abandonedAt');
        const reason = reasonRaw.trim();
        if (reason.length === 0 || reason.length > 500 || /[\u0000-\u001f\u007f]/u.test(reason)) {
          throw new DomainError('DOMAIN_INVALID', 'reason must be nonempty, bounded, and free of control characters');
        }
        const earlier = startedAt ?? createdAt;
        if (startedAt !== null && Date.parse(startedAt) < Date.parse(createdAt)) {
          throw new DomainError('DOMAIN_INVALID', 'startedAt precedes createdAt');
        }
        if (Date.parse(abandonedAt) < Date.parse(earlier)) {
          throw new DomainError('DOMAIN_INVALID', 'abandonedAt precedes the current state');
        }
        return { id, status, topic, plannedMinutes, createdAt, startedAt, abandonedAt, reason };
      }
      default:
        issues.push({ path: `${path}.status`, message: `unsupported status ${status}` });
        return undefined;
    }
  } catch (error: unknown) {
    issues.push({ path, message: error instanceof Error ? error.message : 'invalid session' });
    return undefined;
  }
}

export function decodeLedger(text: string): StudyLedger {
  let parsed: unknown;
  try {
    parsed = JSON.parse(text) as unknown;
  } catch (error: unknown) {
    throw new StorageValidationError([{ path: '$', message: 'invalid JSON' }], { cause: error });
  }
  const issues: ValidationIssue[] = [];
  if (!isRecord(parsed)) throw new StorageValidationError([{ path: '$', message: 'expected an object' }]);
  addUnknownKeyIssues(parsed, ROOT_KEYS, '$', issues);
  if (parsed['format'] !== FORMAT) issues.push({ path: '$.format', message: `expected ${FORMAT}` });
  const nextIdRaw = parsed['nextId'];
  if (typeof nextIdRaw !== 'number' || !Number.isSafeInteger(nextIdRaw) || nextIdRaw <= 0) {
    issues.push({ path: '$.nextId', message: 'expected a positive safe integer' });
  }
  const sessionsRaw = parsed['sessions'];
  if (!Array.isArray(sessionsRaw)) {
    issues.push({ path: '$.sessions', message: 'expected an array' });
    throw new StorageValidationError(issues);
  }
  const sessions = sessionsRaw
    .map((raw, index) => decodeSession(raw, index, issues))
    .filter((session): session is StudySession => session !== undefined);

  const seen = new Map<number, number>();
  for (const [index, session] of sessions.entries()) {
    const first = seen.get(session.id);
    if (first !== undefined) {
      issues.push({ path: `$.sessions[${index}].id`, message: `duplicates session ${session.id} from index ${first}` });
    } else {
      seen.set(session.id, index);
    }
  }
  const nextId = typeof nextIdRaw === 'number' && Number.isSafeInteger(nextIdRaw) && nextIdRaw > 0
    ? nextIdRaw
    : undefined;
  const maxId = sessions.reduce((maximum, session) => Math.max(maximum, session.id), 0);
  if (nextId !== undefined && nextId <= maxId) {
    issues.push({ path: '$.nextId', message: `must be greater than existing maximum id ${maxId}` });
  }
  if (issues.length > 0 || nextId === undefined) throw new StorageValidationError(issues);
  return { nextId, sessions: [...sessions].sort((left, right) => left.id - right.id) };
}

export function encodeLedger(ledger: StudyLedger): string {
  const canonical = {
    format: FORMAT,
    nextId: ledger.nextId,
    sessions: [...ledger.sessions].sort((left, right) => left.id - right.id),
  };
  return `${JSON.stringify(canonical, null, 2)}\n`;
}
