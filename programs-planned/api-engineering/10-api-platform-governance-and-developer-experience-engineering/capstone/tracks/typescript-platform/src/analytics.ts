export interface UsageEvent { at: string; consumerId: string; apiRef: string; version: string; event: string; }

export function productMetrics(events: UsageEvent[], deprecatedVersions: Set<string>) {
  const issued = new Map<string, number>(); const first: number[] = []; const active = new Set<string>(); let deprecatedUses = 0;
  for (const event of [...events].sort((a,b) => a.at.localeCompare(b.at))) {
    const key = `${event.consumerId}|${event.apiRef}`;
    if (event.event === "credential_issued") issued.set(key, Date.parse(event.at));
    if (event.event === "first_success" && issued.has(key)) { first.push((Date.parse(event.at)-issued.get(key)!)/1000); active.add(event.consumerId); }
    if (event.event === "active_use") active.add(event.consumerId);
    if (deprecatedVersions.has(`${event.apiRef}@${event.version}`) && ["active_use","first_success"].includes(event.event)) deprecatedUses++;
  }
  first.sort((a,b)=>a-b); const median = first.length ? (first.length%2 ? first[(first.length-1)/2]! : (first[first.length/2-1]!+first[first.length/2]!)/2) : null;
  return { activeConsumers:active.size, medianTimeToFirstSuccessSeconds:median, deprecatedVersionUses:deprecatedUses };
}
