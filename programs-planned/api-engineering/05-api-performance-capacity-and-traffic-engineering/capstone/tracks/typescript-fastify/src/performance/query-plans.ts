export interface PlanSummary {
  actualRows: bigint;
  estimatedRows: bigint;
  sharedHitBlocks: bigint;
  sharedReadBlocks: bigint;
  tempReadBlocks: bigint;
  tempWrittenBlocks: bigint;
  sequentialScans: string[];
  indexScans: string[];
  sortNodes: number;
  diskSorts: number;
  totalNodes: number;
}

type PlanNode = Record<string, unknown>;

function asNode(value: unknown): PlanNode {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new Error("plan node must be an object");
  }
  return value as PlanNode;
}

function root(document: unknown): PlanNode {
  if (Array.isArray(document) && document.length === 1) {
    const first = asNode(document[0]);
    if ("Plan" in first) return asNode(first.Plan);
  }
  const object = asNode(document);
  if ("Plan" in object) return asNode(object.Plan);
  if ("Node Type" in object) return object;
  throw new Error("unrecognized PostgreSQL JSON plan");
}

function count(node: PlanNode, key: string): bigint {
  const value = node[key] ?? 0;
  if (typeof value === "number") {
    if (!Number.isSafeInteger(value) || value < 0) throw new Error(`invalid ${key}`);
    return BigInt(value);
  }
  if (typeof value === "string" && /^[0-9]+$/.test(value)) return BigInt(value);
  throw new Error(`invalid ${key}`);
}

function walk(node: PlanNode, output: PlanNode[]): void {
  output.push(node);
  const children = node.Plans ?? [];
  if (!Array.isArray(children)) throw new Error("Plans must be an array");
  for (const child of children) walk(asNode(child), output);
}

export function summarizePlan(document: unknown): PlanSummary {
  const nodes: PlanNode[] = [];
  const planRoot = root(document);
  walk(planRoot, nodes);
  const sequentialScans: string[] = [];
  const indexScans: string[] = [];
  let sortNodes = 0;
  let diskSorts = 0;
  for (const node of nodes) {
    const type = String(node["Node Type"] ?? "");
    const relation = String(node["Relation Name"] ?? "<unknown>");
    if (type === "Seq Scan") sequentialScans.push(relation);
    if (type.includes("Index") || type === "Bitmap Heap Scan") {
      indexScans.push(String(node["Index Name"] ?? relation));
    }
    if (type === "Sort") {
      sortNodes += 1;
      if (String(node["Sort Method"] ?? "").includes("Disk")) diskSorts += 1;
    }
  }
  const sum = (key: string): bigint =>
    nodes.reduce((total, node) => total + count(node, key), 0n);
  return {
    actualRows: count(planRoot, "Actual Rows"),
    estimatedRows: count(planRoot, "Plan Rows"),
    sharedHitBlocks: sum("Shared Hit Blocks"),
    sharedReadBlocks: sum("Shared Read Blocks"),
    tempReadBlocks: sum("Temp Read Blocks"),
    tempWrittenBlocks: sum("Temp Written Blocks"),
    sequentialScans,
    indexScans,
    sortNodes,
    diskSorts,
    totalNodes: nodes.length,
  };
}

export function possibleConnections(input: {
  apiInstances: number;
  apiPoolMax: number;
  workers: number;
  workerPoolMax: number;
  operationalReserve: number;
}): number {
  for (const value of Object.values(input)) {
    if (!Number.isSafeInteger(value) || value < 0) throw new Error("invalid connection budget");
  }
  return (
    input.apiInstances * input.apiPoolMax +
    input.workers * input.workerPoolMax +
    input.operationalReserve
  );
}
