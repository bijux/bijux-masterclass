import {
  abandonSession,
  completeSession,
  findSession,
  listSessions,
  planSession,
  searchSessions,
  startSession,
  summarizeLedger,
  type StudyLedger,
} from './domain.js';
import type { Command } from './command.js';
import { renderHelp, renderSession, renderSessionList, renderSummary } from './render.js';

export interface AppDependencies {
  readonly dataPath: string;
  readonly now: () => Date;
  readonly load: (path: string) => Promise<StudyLedger>;
  readonly save: (path: string, ledger: StudyLedger) => Promise<void>;
}

export interface AppResult {
  readonly stdout: string;
  readonly exitCode: 0;
}

function timestamp(dependencies: AppDependencies): string {
  return dependencies.now().toISOString();
}

async function persist(
  dependencies: AppDependencies,
  ledger: StudyLedger,
  success: string,
): Promise<AppResult> {
  await dependencies.save(dependencies.dataPath, ledger);
  return { stdout: success, exitCode: 0 };
}

export async function executeCommand(command: Command, dependencies: AppDependencies): Promise<AppResult> {
  if (command.kind === 'help') return { stdout: renderHelp(), exitCode: 0 };
  if (command.kind === 'version') return { stdout: 'studyledger 1.0.0\n', exitCode: 0 };

  const ledger = await dependencies.load(dependencies.dataPath);
  switch (command.kind) {
    case 'plan': {
      const next = planSession(ledger, command.topic, command.minutes, timestamp(dependencies));
      const created = next.sessions.at(-1);
      if (created === undefined) throw new Error('plan invariant failed');
      return persist(dependencies, next, `planned\t${created.id}\t${created.topic}\n`);
    }
    case 'start':
      return persist(
        dependencies,
        startSession(ledger, command.id, timestamp(dependencies)),
        `started\t${command.id}\n`,
      );
    case 'complete':
      return persist(
        dependencies,
        completeSession(ledger, command.id, command.minutes, timestamp(dependencies), command.note),
        `completed\t${command.id}\n`,
      );
    case 'abandon':
      return persist(
        dependencies,
        abandonSession(ledger, command.id, timestamp(dependencies), command.reason),
        `abandoned\t${command.id}\n`,
      );
    case 'list':
      return { stdout: renderSessionList(listSessions(ledger, command.status)), exitCode: 0 };
    case 'show':
      return { stdout: renderSession(findSession(ledger, command.id)), exitCode: 0 };
    case 'search':
      return { stdout: renderSessionList(searchSessions(ledger, command.query)), exitCode: 0 };
    case 'summary':
      return { stdout: renderSummary(summarizeLedger(ledger)), exitCode: 0 };
  }
}
