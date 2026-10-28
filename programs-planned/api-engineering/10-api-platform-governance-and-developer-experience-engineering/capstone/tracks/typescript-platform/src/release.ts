export interface ReleaseInput {
  catalogValid: boolean; registryValid: boolean; policyDecision: "pass"|"review"|"fail";
  lifecycleSafe: boolean; templateSafe: boolean; docsComplete: boolean;
  sdkTraceable: boolean; runtimeSafe: boolean; sandboxSafe: boolean;
}
export function evaluatePlatformRelease(input: ReleaseInput) {
  const failures: string[] = [];
  for (const [name, ok] of Object.entries({ catalog:input.catalogValid, registry:input.registryValid, lifecycle:input.lifecycleSafe, template:input.templateSafe, documentation:input.docsComplete, sdk:input.sdkTraceable, runtime:input.runtimeSafe, sandbox:input.sandboxSafe })) if (!ok) failures.push(name);
  if (input.policyDecision === "fail") failures.push("policy");
  if (failures.length) return { decision:"rejected", reasons:failures };
  if (input.policyDecision === "review") return { decision:"review", reasons:["approved-exception-or-human-judgment-required"] };
  return { decision:"accepted", reasons:[] };
}
