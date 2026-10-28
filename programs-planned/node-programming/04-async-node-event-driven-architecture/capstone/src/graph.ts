import { GraphError } from './errors.js';
import type { TaskManifest, TaskSpec } from './domain.js';

export class TaskGraph {
  readonly tasks: readonly TaskSpec[];
  readonly positions: ReadonlyMap<string, number>;
  readonly dependents: ReadonlyMap<string, readonly string[]>;
  readonly topologicalOrder: readonly string[];

  private constructor(tasks: readonly TaskSpec[], positions: Map<string, number>, dependents: Map<string, readonly string[]>, order: readonly string[]) {
    this.tasks = tasks; this.positions = positions; this.dependents = dependents; this.topologicalOrder = order;
  }

  static validate(manifest: TaskManifest): TaskGraph {
    const positions = new Map<string, number>();
    manifest.tasks.forEach((task, index) => {
      if (positions.has(task.id)) throw new GraphError(`duplicate task id: ${task.id}`);
      positions.set(task.id, index);
    });
    const dependentsMutable = new Map<string, string[]>();
    for (const task of manifest.tasks) dependentsMutable.set(task.id, []);
    for (const task of manifest.tasks) {
      for (const dependency of task.dependsOn) {
        if (!positions.has(dependency)) throw new GraphError(`task ${task.id} depends on unknown task ${dependency}`);
        if (dependency === task.id) throw new GraphError(`task ${task.id} depends on itself`);
        dependentsMutable.get(dependency)!.push(task.id);
      }
    }
    const indegree = manifest.tasks.map(task => task.dependsOn.length);
    const ready = manifest.tasks.map((task, index) => ({ task, index })).filter(entry => indegree[entry.index] === 0);
    ready.sort((a, b) => a.index - b.index);
    const order: string[] = [];
    while (ready.length > 0) {
      const entry = ready.shift()!;
      order.push(entry.task.id);
      for (const dependentId of dependentsMutable.get(entry.task.id)!) {
        const index = positions.get(dependentId)!;
        const nextIndegree = (indegree[index] ?? 0) - 1;
        indegree[index] = nextIndegree;
        if (nextIndegree === 0) {
          ready.push({ task: manifest.tasks[index]!, index });
          ready.sort((a, b) => a.index - b.index);
        }
      }
    }
    if (order.length !== manifest.tasks.length) {
      const unresolved = manifest.tasks.filter((_, index) => indegree[index]! > 0).map(task => task.id);
      throw new GraphError(`dependency cycle includes: ${unresolved.join(', ')}`);
    }
    const dependents = new Map<string, readonly string[]>();
    for (const [id, values] of dependentsMutable) dependents.set(id, Object.freeze([...values]));
    return new TaskGraph(manifest.tasks, positions, dependents, Object.freeze(order));
  }
}
