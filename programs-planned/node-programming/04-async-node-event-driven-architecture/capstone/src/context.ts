import { AsyncLocalStorage } from 'node:async_hooks';
import { channel, type ChannelListener } from 'node:diagnostics_channel';

export interface TaskContext { readonly runId: string; readonly taskId?: string; readonly index?: number; }
export interface TaskDiagnostic { readonly phase: 'start' | 'end' | 'error'; readonly context: TaskContext; readonly error?: unknown; }
const rawTaskDiagnostics = channel('bijux.taskharbor.task');
export const taskDiagnostics = {
  get hasSubscribers(): boolean { return rawTaskDiagnostics.hasSubscribers; },
  publish(message: TaskDiagnostic): void { rawTaskDiagnostics.publish(message); },
  subscribe(listener: (message: TaskDiagnostic) => void): void { rawTaskDiagnostics.subscribe(listener as ChannelListener); },
  unsubscribe(listener: (message: TaskDiagnostic) => void): void { rawTaskDiagnostics.unsubscribe(listener as ChannelListener); },
};

function publish(message: TaskDiagnostic): void {
  if (!taskDiagnostics.hasSubscribers) return;
  try { taskDiagnostics.publish(message); } catch { /* diagnostics never own task behavior */ }
}

export class TaskContextManager {
  #storage = new AsyncLocalStorage<TaskContext>();
  current(): TaskContext | undefined { return this.#storage.getStore(); }
  run<T>(context: TaskContext, operation: () => Promise<T>): Promise<T> {
    const frozen = Object.freeze({ ...context });
    return this.#storage.run(frozen, async () => {
      publish({ phase: 'start', context: frozen });
      try { const value = await operation(); publish({ phase: 'end', context: frozen }); return value; }
      catch (error) { publish({ phase: 'error', context: frozen, error }); throw error; }
    });
  }
}
