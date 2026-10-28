import { DomainError } from './errors.js';

export type SessionStatus = 'planned' | 'active' | 'completed' | 'abandoned';

interface BaseSession {
  readonly id: number;
  readonly topic: string;
  readonly plannedMinutes: number;
  readonly createdAt: string;
}

export interface PlannedSession extends BaseSession {
  readonly status: 'planned';
}

export interface ActiveSession extends BaseSession {
  readonly status: 'active';
  readonly startedAt: string;
}

export interface CompletedSession extends BaseSession {
  readonly status: 'completed';
  readonly startedAt: string;
  readonly completedAt: string;
  readonly actualMinutes: number;
  readonly note: string | null;
}

export interface AbandonedSession extends BaseSession {
  readonly status: 'abandoned';
  readonly startedAt: string | null;
  readonly abandonedAt: string;
  readonly reason: string;
}

export type StudySession = PlannedSession | ActiveSession | CompletedSession | AbandonedSession;

export interface StudyLedger {
  readonly nextId: number;
  readonly sessions: readonly StudySession[];
}

export interface LedgerSummary {
  readonly total: number;
  readonly planned: number;
  readonly active: number;
  readonly completed: number;
  readonly abandoned: number;
  readonly plannedMinutes: number;
  readonly completedMinutes: number;
}

const MAX_TOPIC_LENGTH = 200;
const MAX_NOTE_LENGTH = 2_000;
const MAX_REASON_LENGTH = 500;
const MAX_PLANNED_MINUTES = 1_440;
const MAX_ACTUAL_MINUTES = 2_880;

export function emptyLedger(): StudyLedger {
  return { nextId: 1, sessions: [] };
}

function rejectControlCharacters(value: string, label: string): void {
  if (/[\u0000-\u001f\u007f]/u.test(value)) {
    throw new DomainError('DOMAIN_INVALID', `${label} must not contain control characters`);
  }
}

export function normalizeTopic(raw: string): string {
  const topic = raw.trim();
  if (topic.length === 0) {
    throw new DomainError('DOMAIN_INVALID', 'topic must not be empty');
  }
  if (topic.length > MAX_TOPIC_LENGTH) {
    throw new DomainError('DOMAIN_INVALID', `topic must not exceed ${MAX_TOPIC_LENGTH} characters`);
  }
  rejectControlCharacters(topic, 'topic');
  return topic;
}

function normalizeOptionalNote(raw: string | undefined): string | null {
  if (raw === undefined) return null;
  const note = raw.trim();
  if (note.length === 0) return null;
  if (note.length > MAX_NOTE_LENGTH) {
    throw new DomainError('DOMAIN_INVALID', `note must not exceed ${MAX_NOTE_LENGTH} characters`);
  }
  rejectControlCharacters(note, 'note');
  return note;
}

function normalizeReason(raw: string): string {
  const reason = raw.trim();
  if (reason.length === 0) {
    throw new DomainError('DOMAIN_INVALID', 'reason must not be empty');
  }
  if (reason.length > MAX_REASON_LENGTH) {
    throw new DomainError('DOMAIN_INVALID', `reason must not exceed ${MAX_REASON_LENGTH} characters`);
  }
  rejectControlCharacters(reason, 'reason');
  return reason;
}

export function validateSessionId(id: number): number {
  if (!Number.isSafeInteger(id) || id <= 0) {
    throw new DomainError('DOMAIN_INVALID', 'session id must be a positive safe integer');
  }
  return id;
}

export function validatePlannedMinutes(minutes: number): number {
  if (!Number.isSafeInteger(minutes) || minutes < 1 || minutes > MAX_PLANNED_MINUTES) {
    throw new DomainError(
      'DOMAIN_INVALID',
      `planned minutes must be an integer from 1 to ${MAX_PLANNED_MINUTES}`,
    );
  }
  return minutes;
}

export function validateActualMinutes(minutes: number): number {
  if (!Number.isSafeInteger(minutes) || minutes < 1 || minutes > MAX_ACTUAL_MINUTES) {
    throw new DomainError(
      'DOMAIN_INVALID',
      `actual minutes must be an integer from 1 to ${MAX_ACTUAL_MINUTES}`,
    );
  }
  return minutes;
}

export function normalizeTimestamp(raw: string, label = 'timestamp'): string {
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/u.test(raw)) {
    throw new DomainError('DOMAIN_INVALID', `${label} must be a canonical UTC ISO timestamp`);
  }
  const time = new Date(raw);
  if (!Number.isFinite(time.valueOf()) || time.toISOString() !== raw) {
    throw new DomainError('DOMAIN_INVALID', `${label} must be a real canonical UTC ISO timestamp`);
  }
  return raw;
}

function assertChronology(earlier: string, later: string, message: string): void {
  if (Date.parse(later) < Date.parse(earlier)) {
    throw new DomainError('DOMAIN_INVALID', message);
  }
}

export function findSession(ledger: StudyLedger, id: number): StudySession {
  validateSessionId(id);
  const session = ledger.sessions.find((candidate) => candidate.id === id);
  if (session === undefined) {
    throw new DomainError('DOMAIN_MISSING', `session ${id} does not exist`);
  }
  return session;
}

function replaceSession(
  ledger: StudyLedger,
  id: number,
  transition: (session: StudySession) => StudySession,
): StudyLedger {
  let found = false;
  const sessions = ledger.sessions.map((session) => {
    if (session.id !== id) return session;
    found = true;
    return transition(session);
  });
  if (!found) {
    throw new DomainError('DOMAIN_MISSING', `session ${id} does not exist`);
  }
  return { ...ledger, sessions };
}

export function planSession(
  ledger: StudyLedger,
  rawTopic: string,
  rawMinutes: number,
  rawCreatedAt: string,
): StudyLedger {
  if (!Number.isSafeInteger(ledger.nextId) || ledger.nextId <= 0 || ledger.nextId >= Number.MAX_SAFE_INTEGER) {
    throw new DomainError('DOMAIN_INVALID', 'session id space is exhausted or invalid');
  }
  const session: PlannedSession = {
    id: ledger.nextId,
    status: 'planned',
    topic: normalizeTopic(rawTopic),
    plannedMinutes: validatePlannedMinutes(rawMinutes),
    createdAt: normalizeTimestamp(rawCreatedAt, 'createdAt'),
  };
  return { nextId: ledger.nextId + 1, sessions: [...ledger.sessions, session] };
}

export function startSession(ledger: StudyLedger, id: number, rawStartedAt: string): StudyLedger {
  const startedAt = normalizeTimestamp(rawStartedAt, 'startedAt');
  return replaceSession(ledger, validateSessionId(id), (session) => {
    if (session.status !== 'planned') {
      throw new DomainError('DOMAIN_TRANSITION', `cannot start a ${session.status} session`);
    }
    assertChronology(session.createdAt, startedAt, 'startedAt must not precede createdAt');
    return { ...session, status: 'active', startedAt };
  });
}

export function completeSession(
  ledger: StudyLedger,
  id: number,
  rawActualMinutes: number,
  rawCompletedAt: string,
  rawNote?: string,
): StudyLedger {
  const completedAt = normalizeTimestamp(rawCompletedAt, 'completedAt');
  const actualMinutes = validateActualMinutes(rawActualMinutes);
  const note = normalizeOptionalNote(rawNote);
  return replaceSession(ledger, validateSessionId(id), (session) => {
    if (session.status !== 'active') {
      throw new DomainError('DOMAIN_TRANSITION', `cannot complete a ${session.status} session`);
    }
    assertChronology(session.startedAt, completedAt, 'completedAt must not precede startedAt');
    return { ...session, status: 'completed', actualMinutes, completedAt, note };
  });
}

export function abandonSession(
  ledger: StudyLedger,
  id: number,
  rawAbandonedAt: string,
  rawReason: string,
): StudyLedger {
  const abandonedAt = normalizeTimestamp(rawAbandonedAt, 'abandonedAt');
  const reason = normalizeReason(rawReason);
  return replaceSession(ledger, validateSessionId(id), (session) => {
    if (session.status !== 'planned' && session.status !== 'active') {
      throw new DomainError('DOMAIN_TRANSITION', `cannot abandon a ${session.status} session`);
    }
    const earlier = session.status === 'active' ? session.startedAt : session.createdAt;
    assertChronology(earlier, abandonedAt, 'abandonedAt must not precede the current session state');
    return {
      id: session.id,
      status: 'abandoned',
      topic: session.topic,
      plannedMinutes: session.plannedMinutes,
      createdAt: session.createdAt,
      startedAt: session.status === 'active' ? session.startedAt : null,
      abandonedAt,
      reason,
    };
  });
}

export function listSessions(ledger: StudyLedger, status?: SessionStatus): readonly StudySession[] {
  const sessions = status === undefined
    ? ledger.sessions
    : ledger.sessions.filter((session) => session.status === status);
  return [...sessions].sort((left, right) => left.id - right.id);
}

export function searchSessions(ledger: StudyLedger, rawQuery: string): readonly StudySession[] {
  const query = rawQuery.trim().toLocaleLowerCase('en');
  if (query.length === 0) {
    throw new DomainError('DOMAIN_INVALID', 'search query must not be empty');
  }
  return ledger.sessions
    .filter((session) => {
      const text = session.status === 'completed' && session.note !== null
        ? `${session.topic}\n${session.note}`
        : session.status === 'abandoned'
          ? `${session.topic}\n${session.reason}`
          : session.topic;
      return text.toLocaleLowerCase('en').includes(query);
    })
    .sort((left, right) => left.id - right.id);
}

export function summarizeLedger(ledger: StudyLedger): LedgerSummary {
  const summary: {
    total: number;
    planned: number;
    active: number;
    completed: number;
    abandoned: number;
    plannedMinutes: number;
    completedMinutes: number;
  } = {
    total: ledger.sessions.length,
    planned: 0,
    active: 0,
    completed: 0,
    abandoned: 0,
    plannedMinutes: 0,
    completedMinutes: 0,
  };
  for (const session of ledger.sessions) {
    summary[session.status] += 1;
    summary.plannedMinutes += session.plannedMinutes;
    if (session.status === 'completed') summary.completedMinutes += session.actualMinutes;
  }
  return summary;
}
