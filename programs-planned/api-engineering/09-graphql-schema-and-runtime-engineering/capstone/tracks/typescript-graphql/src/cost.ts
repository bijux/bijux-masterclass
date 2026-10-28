/** Dependency-light demand analysis for registered GraphQL operations. */

import { ValidationError } from "./model.js";
import type { Document, Selection } from "./operation.js";

export interface CostPolicy {
  maxDepth: number;
  maxAliases: number;
  maxRootFields: number;
  maxCost: number;
  maxFanout: number;
  defaultPageSize: number;
  maxPageSize: number;
}

export interface CostReport {
  depth: number;
  aliases: number;
  rootFields: number;
  estimatedCost: number;
  serviceFanout: number;
}

export const defaultCostPolicy: CostPolicy = {
  maxDepth: 12,
  maxAliases: 30,
  maxRootFields: 8,
  maxCost: 5_000,
  maxFanout: 12,
  defaultPageSize: 20,
  maxPageSize: 100,
};

const serviceFields: Readonly<Record<string, string>> = {
  project: "analysis-control",
  analysisRun: "analysis-control",
  analysisRuns: "analysis-control",
  artifact: "artifact-service",
  artifacts: "artifact-service",
  deliverySummary: "notification-service",
};

const listFields = new Set([
  "analysisRuns",
  "search",
  "edges",
  "artifacts",
]);

const baseCost: Readonly<Record<string, number>> = {
  search: 8,
  analysisRuns: 5,
  artifacts: 5,
  deliverySummary: 3,
};

function pageSize(
  arguments_: readonly string[],
  variables: Readonly<Record<string, unknown>>,
  policy: CostPolicy,
): number {
  for (let index = 0; index < arguments_.length; index += 1) {
    if (
      arguments_[index] !== "first" ||
      arguments_[index + 1] !== ":"
    ) {
      continue;
    }

    let raw: unknown = arguments_[index + 2];
    if (raw === "$" && arguments_[index + 3]) {
      raw = variables[arguments_[index + 3]!];
    } else if (typeof raw === "string" && raw.startsWith("$")) {
      raw = variables[raw.slice(1)];
    }

    const size =
      raw === undefined ? policy.defaultPageSize : Number(raw);
    if (
      !Number.isSafeInteger(size) ||
      size < 1 ||
      size > policy.maxPageSize
    ) {
      throw new ValidationError("page size outside policy");
    }
    return size;
  }

  return policy.defaultPageSize;
}

export function analyze(
  document: Document,
  operationName: string,
  variables: Readonly<Record<string, unknown>> = {},
  policy: CostPolicy = defaultCostPolicy,
): CostReport {
  const matches = document.operations.filter(
    (operation) => operation.name === operationName,
  );
  if (matches.length !== 1) {
    throw new ValidationError(
      "operation name must select exactly one operation",
    );
  }

  const operation = matches[0]!;
  const services = new Set<string>();
  let aliases = 0;
  let maximumDepth = 0;
  let estimatedCost = 0;

  function visit(
    selections: readonly Selection[],
    depth: number,
    fragmentStack: readonly string[],
    multiplier = 1,
  ): void {
    maximumDepth = Math.max(maximumDepth, depth);

    for (const selection of selections) {
      if (selection.kind === "spread") {
        if (fragmentStack.includes(selection.name)) {
          throw new ValidationError("fragment cycle");
        }
        const fragment = document.fragments.get(selection.name);
        if (!fragment) {
          throw new ValidationError("undefined fragment");
        }
        visit(
          fragment.selections,
          depth,
          [...fragmentStack, selection.name],
          multiplier,
        );
        continue;
      }

      if (selection.kind === "inline") {
        visit(
          selection.selections,
          depth,
          fragmentStack,
          multiplier,
        );
        continue;
      }

      if (selection.alias) {
        aliases += 1;
      }

      const service = serviceFields[selection.name];
      if (service) {
        services.add(service);
      }

      let childMultiplier = multiplier;
      if (listFields.has(selection.name)) {
        childMultiplier *= pageSize(
          selection.arguments,
          variables,
          policy,
        );
      }

      estimatedCost +=
        (baseCost[selection.name] ?? 1) * multiplier;

      if (selection.selections.length > 0) {
        visit(
          selection.selections,
          depth + 1,
          fragmentStack,
          childMultiplier,
        );
      }
    }
  }

  visit(operation.selections, 1, []);

  const report: CostReport = {
    depth: maximumDepth,
    aliases,
    rootFields: operation.selections.length,
    estimatedCost,
    serviceFanout: services.size,
  };

  if (report.depth > policy.maxDepth) {
    throw new ValidationError("query depth exceeds budget");
  }
  if (report.aliases > policy.maxAliases) {
    throw new ValidationError("alias count exceeds budget");
  }
  if (report.rootFields > policy.maxRootFields) {
    throw new ValidationError("root field count exceeds budget");
  }
  if (report.estimatedCost > policy.maxCost) {
    throw new ValidationError("estimated cost exceeds budget");
  }
  if (report.serviceFanout > policy.maxFanout) {
    throw new ValidationError("service fanout exceeds budget");
  }

  return report;
}
