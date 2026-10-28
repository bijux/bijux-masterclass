export interface Route { id: string; host: string; pathPrefix: string; apiRef: string; release: string; edgeAuthn: string; domainAuthz: string; rateClass: string; }

export function validateRoute(route: Route): void {
  if (!["owner-service","graph-and-owner-services"].includes(route.domainAuthz)) throw new Error("domain-policy-at-edge");
  if (!route.host.endsWith(".example.invalid")) throw new Error("unexpected-course-host");
  if (!["oauth2","mtls"].includes(route.edgeAuthn)) throw new Error("unsupported-edge-authn");
}

export function routeDrift(desired: Route[], current: Route[]) {
  const d = new Map(desired.map((r) => [r.id, r])); const c = new Map(current.map((r) => [r.id, r]));
  const missing = [...d.keys()].filter((k) => !c.has(k)).sort();
  const extra = [...c.keys()].filter((k) => !d.has(k)).sort();
  const changed = [...d.keys()].filter((k) => c.has(k) && JSON.stringify(d.get(k)) !== JSON.stringify(c.get(k))).sort();
  return { missing, extra, changed, inSync: !(missing.length || extra.length || changed.length) };
}
