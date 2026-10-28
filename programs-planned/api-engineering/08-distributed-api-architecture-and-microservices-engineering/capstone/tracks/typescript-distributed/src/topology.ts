import { ValidationError } from "./model.js";

export interface SyncEdge {
  source: string;
  target: string;
  purpose: string;
  budgetMs: number;
}

export class DependencyGraph {
  constructor(readonly edges: SyncEdge[] = []) {}

  adjacency(): Map<string, string[]> {
    const graph = new Map<string, string[]>();
    for (const edge of this.edges) {
      if (edge.source === edge.target) {
        throw new ValidationError("self dependency is forbidden");
      }
      if (edge.budgetMs <= 0) {
        throw new ValidationError("edge budget must be positive");
      }
      graph.set(edge.source, [...(graph.get(edge.source) ?? []), edge.target]);
      if (!graph.has(edge.target)) graph.set(edge.target, []);
    }
    return graph;
  }

  cycle(): string[] | undefined {
    const graph = this.adjacency();
    const visiting = new Set<string>();
    const visited = new Set<string>();
    const stack: string[] = [];

    const visit = (node: string): string[] | undefined => {
      if (visiting.has(node)) {
        return [...stack.slice(stack.indexOf(node)), node];
      }
      if (visited.has(node)) return undefined;
      visiting.add(node);
      stack.push(node);
      for (const next of graph.get(node) ?? []) {
        const found = visit(next);
        if (found) return found;
      }
      stack.pop();
      visiting.delete(node);
      visited.add(node);
      return undefined;
    };

    for (const node of graph.keys()) {
      const found = visit(node);
      if (found) return found;
    }
    return undefined;
  }

  longestDepth(root: string): number {
    if (this.cycle()) {
      throw new ValidationError("depth undefined for cyclic graph");
    }
    const graph = this.adjacency();
    const memo = new Map<string, number>();
    const depth = (node: string): number => {
      const cached = memo.get(node);
      if (cached !== undefined) return cached;
      const children = graph.get(node) ?? [];
      const value = children.length === 0
        ? 0
        : 1 + Math.max(...children.map(depth));
      memo.set(node, value);
      return value;
    };
    return depth(root);
  }

  validate(maxPublicDepth: number, forbidden: ReadonlySet<string>): void {
    const cycle = this.cycle();
    if (cycle) {
      throw new ValidationError(`synchronous cycle: ${cycle.join(" -> ")}`);
    }
    for (const edge of this.edges) {
      if (forbidden.has(`${edge.source}->${edge.target}`)) {
        throw new ValidationError(
          `forbidden synchronous edge: ${edge.source}->${edge.target}`,
        );
      }
    }
    if (this.longestDepth("edge-gateway") > maxPublicDepth) {
      throw new ValidationError("public synchronous depth exceeds policy");
    }
  }
}

export function serialAvailability(values: readonly number[]): number {
  if (values.some((value) => value < 0 || value > 1)) {
    throw new ValidationError("invalid availability");
  }
  return values.reduce((total, value) => total * value, 1);
}

export function serialLatencyMs(values: readonly number[]): number {
  if (values.some((value) => value < 0)) {
    throw new ValidationError("latency cannot be negative");
  }
  return values.reduce((total, value) => total + value, 0);
}

export function parallelLatencyMs(values: readonly number[]): number {
  return values.length === 0 ? 0 : Math.max(...values);
}
