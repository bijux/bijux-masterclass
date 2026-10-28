import type { Clock } from './clock.js';
import type { TaskSpec } from './domain.js';
import { TaskExecutionError } from './errors.js';

export interface TaskExecutor { execute(task: TaskSpec, signal: AbortSignal): Promise<string>; }

export class BuiltinTaskExecutor implements TaskExecutor {
  constructor(private readonly clock: Clock) {}
  async execute(task: TaskSpec, signal: AbortSignal): Promise<string> {
    signal.throwIfAborted();
    switch (task.kind) {
      case 'delay': await this.clock.sleep(task.milliseconds, signal); return `delayed:${task.milliseconds}`;
      case 'echo': return task.text;
      case 'uppercase': return task.text.toUpperCase();
      case 'fail': throw new TaskExecutionError(task.id, task.message);
    }
  }
}
