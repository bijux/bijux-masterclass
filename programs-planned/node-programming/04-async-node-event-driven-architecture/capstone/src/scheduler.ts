import { randomUUID } from 'node:crypto';
import type { Clock } from './clock.js';
import { SystemClock } from './clock.js';
import { TaskContextManager } from './context.js';
import type { FailurePolicy, RunSummary, TaskOutcome, TaskSpec } from './domain.js';
import { priorityRank } from './domain.js';
import { FailFastError, RunTimeoutError, TaskTimeoutError } from './errors.js';
import { HarborEventHub } from './events.js';
import type { TaskExecutor } from './executor.js';
import { BuiltinTaskExecutor } from './executor.js';
import type { TaskGraph } from './graph.js';

export interface RunOptions {
  readonly concurrency: number;
  readonly policy: FailurePolicy;
  readonly signal?: AbortSignal;
  readonly timeoutMs?: number;
  readonly runId?: string;
  readonly clock?: Clock;
  readonly executor?: TaskExecutor;
  readonly events?: HarborEventHub;
  readonly contexts?: TaskContextManager;
}

type InternalState = 'pending' | 'ready' | 'running' | 'terminal';
interface Completion { readonly index: number; readonly outcome: TaskOutcome; }

function linkSignal(parent: AbortSignal | undefined, controller: AbortController): () => void {
  if (!parent) return () => undefined;
  const forward = (): void => controller.abort(parent.reason);
  if (parent.aborted) forward(); else parent.addEventListener('abort', forward, { once: true });
  return () => parent.removeEventListener('abort', forward);
}

function duration(clock: Clock, start: number): number { return Math.max(0, clock.now() - start); }

async function executeOne(
  task: TaskSpec,
  index: number,
  runId: string,
  runSignal: AbortSignal,
  clock: Clock,
  executor: TaskExecutor,
  contexts: TaskContextManager,
): Promise<Completion> {
  const started = clock.now();
  const controller = new AbortController();
  const unlink = linkSignal(runSignal, controller);
  const timeoutController = new AbortController();
  let timeoutPromise: Promise<void> | undefined;
  if (task.timeoutMs !== undefined) {
    timeoutPromise = clock.sleep(task.timeoutMs, timeoutController.signal).then(() => {
      controller.abort(new TaskTimeoutError(task.id, task.timeoutMs!));
    }, error => {
      if (!timeoutController.signal.aborted) throw error;
    });
  }
  try {
    const value = await contexts.run({ runId, taskId: task.id, index }, () => executor.execute(task, controller.signal));
    return { index, outcome: { id: task.id, index, status: 'succeeded', value, durationMs: duration(clock, started) } };
  } catch (error) {
    if (controller.signal.aborted) {
      const reason = controller.signal.reason;
      if (reason instanceof TaskTimeoutError) {
        return { index, outcome: { id: task.id, index, status: 'timed-out', error: reason, durationMs: duration(clock, started) } };
      }
      return { index, outcome: { id: task.id, index, status: 'cancelled', reason, durationMs: duration(clock, started) } };
    }
    return { index, outcome: { id: task.id, index, status: 'failed', error, durationMs: duration(clock, started) } };
  } finally {
    timeoutController.abort(new Error('task completed'));
    await timeoutPromise?.catch(() => undefined);
    unlink();
  }
}

export async function runGraph(graph: TaskGraph, options: RunOptions): Promise<RunSummary> {
  if (!Number.isInteger(options.concurrency) || options.concurrency <= 0) throw new RangeError('concurrency must be positive');
  if (options.timeoutMs !== undefined && (!Number.isInteger(options.timeoutMs) || options.timeoutMs <= 0)) throw new RangeError('timeoutMs must be positive');
  const runId = options.runId ?? randomUUID();
  const clock = options.clock ?? new SystemClock();
  const executor = options.executor ?? new BuiltinTaskExecutor(clock);
  const events = options.events ?? new HarborEventHub();
  const contexts = options.contexts ?? new TaskContextManager();
  const runController = new AbortController();
  const unlink = linkSignal(options.signal, runController);
  const timeoutController = new AbortController();
  let runTimeout: Promise<void> | undefined;
  if (options.timeoutMs !== undefined) {
    runTimeout = clock.sleep(options.timeoutMs, timeoutController.signal).then(() => runController.abort(new RunTimeoutError(options.timeoutMs!)), error => {
      if (!timeoutController.signal.aborted) throw error;
    });
  }
  const started = clock.now();
  const states: InternalState[] = graph.tasks.map(() => 'pending');
  const outcomes: Array<TaskOutcome | undefined> = Array.from({ length: graph.tasks.length }, () => undefined);
  const running = new Map<number, Promise<Completion>>();
  let peakConcurrency = 0;
  const emit = (event: Parameters<HarborEventHub['emit']>[0]): void => { events.emit(event); };
  emit({ type: 'run-started', runId, taskCount: graph.tasks.length });

  function markBlockedAndCancelled(): boolean {
    let changed = false;
    for (let index = 0; index < graph.tasks.length; index += 1) {
      if (states[index] === 'terminal' || states[index] === 'running') continue;
      const task = graph.tasks[index]!;
      const blockedBy = task.dependsOn.filter(id => {
        const outcome = outcomes[graph.positions.get(id)!];
        return outcome !== undefined && outcome.status !== 'succeeded';
      });
      if (blockedBy.length > 0) {
        states[index] = 'terminal';
        outcomes[index] = { id: task.id, index, status: 'blocked', blockedBy, durationMs: 0 };
        emit({ type: 'task-blocked', runId, taskId: task.id, index, blockedBy }); changed = true;
      }
    }
    if (runController.signal.aborted) {
      for (let index = 0; index < graph.tasks.length; index += 1) {
        if (states[index] !== 'pending' && states[index] !== 'ready') continue;
        const task = graph.tasks[index]!;
        states[index] = 'terminal';
        outcomes[index] = { id: task.id, index, status: 'cancelled', reason: runController.signal.reason, durationMs: 0 };
        emit({ type: 'task-cancelled', runId, taskId: task.id, index, reason: runController.signal.reason }); changed = true;
      }
    }
    return changed;
  }

  function refreshReady(): void {
    for (let index = 0; index < graph.tasks.length; index += 1) {
      if (states[index] !== 'pending') continue;
      const task = graph.tasks[index]!;
      if (task.dependsOn.every(id => outcomes[graph.positions.get(id)!]?.status === 'succeeded')) {
        states[index] = 'ready';
        emit({ type: 'task-ready', runId, taskId: task.id, index });
      }
    }
  }

  try {
    while (outcomes.some(value => value === undefined)) {
      markBlockedAndCancelled();
      refreshReady();
      const ready = graph.tasks.map((task, index) => ({ task, index })).filter(entry => states[entry.index] === 'ready');
      ready.sort((a, b) => priorityRank(b.task.priority) - priorityRank(a.task.priority) || a.index - b.index);
      for (const entry of ready) {
        if (running.size >= options.concurrency || runController.signal.aborted) break;
        states[entry.index] = 'running';
        emit({ type: 'task-started', runId, taskId: entry.task.id, index: entry.index });
        running.set(entry.index, executeOne(entry.task, entry.index, runId, runController.signal, clock, executor, contexts));
        peakConcurrency = Math.max(peakConcurrency, running.size);
      }
      if (running.size === 0) {
        markBlockedAndCancelled();
        if (outcomes.some(value => value === undefined)) throw new Error('scheduler made no progress');
        break;
      }
      const completed = await Promise.race(running.values());
      running.delete(completed.index);
      states[completed.index] = 'terminal'; outcomes[completed.index] = completed.outcome;
      const outcome = completed.outcome;
      if (outcome.status === 'succeeded') emit({ type: 'task-succeeded', runId, taskId: outcome.id, index: outcome.index });
      else if (outcome.status === 'failed') emit({ type: 'task-failed', runId, taskId: outcome.id, index: outcome.index, error: outcome.error });
      else if (outcome.status === 'timed-out') emit({ type: 'task-timed-out', runId, taskId: outcome.id, index: outcome.index, error: outcome.error });
      else if (outcome.status === 'cancelled') emit({ type: 'task-cancelled', runId, taskId: outcome.id, index: outcome.index, reason: outcome.reason });
      if (options.policy === 'fail-fast' && (outcome.status === 'failed' || outcome.status === 'timed-out')) {
        runController.abort(new FailFastError(outcome.id));
      }
    }
    await Promise.all(running.values());
    if (outcomes.some(value => value === undefined)) throw new Error('missing terminal outcome');
    emit({ type: 'run-finished', runId });
    return { runId, policy: options.policy, outcomes: outcomes as readonly TaskOutcome[], peakConcurrency, durationMs: duration(clock, started) };
  } finally {
    timeoutController.abort(new Error('run completed'));
    await runTimeout?.catch(() => undefined);
    unlink();
  }
}
