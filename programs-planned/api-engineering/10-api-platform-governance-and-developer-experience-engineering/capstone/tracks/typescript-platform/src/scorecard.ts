const blockingKinds = new Set(["ownership","compatibility","security","reliability"]);
export interface Evidence { entityRef: string; kind: string; status: string; }

export function scorecard(entityRef: string, evidence: Evidence[]) {
  const dimensions: Record<string,string> = {};
  for (const item of evidence) if (item.entityRef === entityRef) dimensions[item.kind] = item.status;
  const blockers = Object.entries(dimensions).filter(([kind,status]) => blockingKinds.has(kind) && status !== "pass").map(([kind])=>kind).sort();
  const reviews = Object.entries(dimensions).filter(([,status])=>status === "review").map(([kind])=>kind).sort();
  return { entityRef, status:blockers.length ? "blocked" : (reviews.length ? "review" : "ready"), dimensions, blockers, reviews };
}
