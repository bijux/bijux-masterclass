import type { LedgerSummary, StudySession } from './domain.js';
import type { StudyLedgerError, StorageValidationError } from './errors.js';

function statusDetail(session: StudySession): string {
  switch (session.status) {
    case 'planned': return '-';
    case 'active': return `started ${session.startedAt}`;
    case 'completed': return `${session.actualMinutes}m at ${session.completedAt}`;
    case 'abandoned': return `at ${session.abandonedAt}: ${session.reason}`;
  }
}

export function renderSessionList(sessions: readonly StudySession[]): string {
  const header = 'id\tstatus\tplanned-minutes\ttopic\tdetail';
  const rows = sessions.map(
    (session) => `${session.id}\t${session.status}\t${session.plannedMinutes}\t${session.topic}\t${statusDetail(session)}`,
  );
  return `${[header, ...rows].join('\n')}\n`;
}

export function renderSession(session: StudySession): string {
  const common = [
    `id\t${session.id}`,
    `status\t${session.status}`,
    `topic\t${session.topic}`,
    `planned-minutes\t${session.plannedMinutes}`,
    `created-at\t${session.createdAt}`,
  ];
  switch (session.status) {
    case 'planned': break;
    case 'active': common.push(`started-at\t${session.startedAt}`); break;
    case 'completed':
      common.push(`started-at\t${session.startedAt}`);
      common.push(`completed-at\t${session.completedAt}`);
      common.push(`actual-minutes\t${session.actualMinutes}`);
      common.push(`note\t${session.note ?? '-'}`);
      break;
    case 'abandoned':
      common.push(`started-at\t${session.startedAt ?? '-'}`);
      common.push(`abandoned-at\t${session.abandonedAt}`);
      common.push(`reason\t${session.reason}`);
      break;
  }
  return `${common.join('\n')}\n`;
}

export function renderSummary(summary: LedgerSummary): string {
  return [
    `total\t${summary.total}`,
    `planned\t${summary.planned}`,
    `active\t${summary.active}`,
    `completed\t${summary.completed}`,
    `abandoned\t${summary.abandoned}`,
    `planned-minutes\t${summary.plannedMinutes}`,
    `completed-minutes\t${summary.completedMinutes}`,
  ].join('\n') + '\n';
}

export function renderHelp(): string {
  return `StudyLedger — a persistent study-session ledger

Usage:
  studiedger plan --topic <text> --minutes <integer>
  studiedger start <id>
  studiedger complete <id> --minutes <integer> [--note <text>]
  studiedger abandon <id> --reason <text>
  studiedger list [--status planned|active|completed|abandoned]
  studiedger show <id>
  studiedger search --query <text>
  studiedger summary
  studiedger help
  studiedger version

Environment:
  STUDY_LEDGER_FILE   override the default ~/.studyledger.json path
`;
}

export function renderError(error: unknown): string {
  if (error instanceof Error) {
    const code = 'code' in error && typeof error.code === 'string' ? error.code : 'UNEXPECTED';
    const lines = [`error\t${code}\t${error.message}`];
    if ('issues' in error && Array.isArray(error.issues)) {
      for (const issue of error.issues as readonly { readonly path: string; readonly message: string }[]) {
        lines.push(`issue\t${issue.path}\t${issue.message}`);
      }
    }
    return `${lines.join('\n')}\n`;
  }
  return `error\tUNEXPECTED\t${String(error)}\n`;
}

// These type-only imports keep the renderer's public error surface documented
// without creating a runtime dependency cycle.
export type RenderedStudyLedgerError = StudyLedgerError | StorageValidationError;
