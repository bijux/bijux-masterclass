import { AsyncLocalStorage } from 'node:async_hooks';
import { channel, type ChannelListener } from 'node:diagnostics_channel';

export interface CorrelationContext {
  readonly runId: string;
  readonly taskId?: string;
  readonly parentTaskId?: string;
}

export interface ContextDiagnostic {
  readonly phase: 'start' | 'end' | 'error';
  readonly context: CorrelationContext;
  readonly error?: unknown;
}

const rawContextDiagnostics = channel('bijux.course4.context');
export const contextDiagnostics = {
  get hasSubscribers(): boolean { return rawContextDiagnostics.hasSubscribers; },
  publish(message: ContextDiagnostic): void { rawContextDiagnostics.publish(message); },
  subscribe(listener: (message: ContextDiagnostic) => void): void {
    rawContextDiagnostics.subscribe(listener as ChannelListener);
  },
  unsubscribe(listener: (message: ContextDiagnostic) => void): void {
    rawContextDiagnostics.unsubscribe(listener as ChannelListener);
  },
};

function publish(message: ContextDiagnostic): void {
  if (!contextDiagnostics.hasSubscribers) return;
  try { contextDiagnostics.publish(message); } catch { /* diagnostics cannot own product failure */ }
}

export class ContextManager {
  #storage = new AsyncLocalStorage<CorrelationContext>();

  current(): CorrelationContext | undefined { return this.#storage.getStore(); }

  async run<T>(context: CorrelationContext, operation: () => Promise<T>): Promise<T> {
    const frozen = Object.freeze({ ...context });
    return this.#storage.run(frozen, async () => {
      publish({ phase: 'start', context: frozen });
      try {
        const value = await operation();
        publish({ phase: 'end', context: frozen });
        return value;
      } catch (error) {
        publish({ phase: 'error', context: frozen, error });
        throw error;
      }
    });
  }

  async child<T>(taskId: string, operation: () => Promise<T>): Promise<T> {
    const parent = this.current();
    if (!parent) throw new Error('no parent context');
    const context: CorrelationContext = parent.taskId
      ? { runId: parent.runId, taskId, parentTaskId: parent.taskId }
      : { runId: parent.runId, taskId };
    return this.run(context, operation);
  }
}
