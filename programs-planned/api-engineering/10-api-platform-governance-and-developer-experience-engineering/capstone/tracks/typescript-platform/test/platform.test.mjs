import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  entityRef, Catalog, ContractRegistry, evaluateFindings, validateException,
  evaluateTransition, deprecationImpact, validateParameters, renderText,
  createSession, validateImport, validateRoute, routeDrift, productMetrics,
  scorecard, evaluatePlatformRelease
} from "../dist/index.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const cap = path.resolve(here, "../../..");
const load = (rel) => JSON.parse(fs.readFileSync(path.join(cap, rel), "utf8"));

test("canonical entity reference", () => {
  assert.equal(entityRef("API","default","analysis-http"),"api:default/analysis-http");
  assert.throws(() => entityRef("API","default","AnalysisHTTP"),/invalid-name/);
});

test("real catalog validates", () => {
  const catalog = new Catalog(load("catalog/entities.json").entities);
  assert.equal(catalog.ownerOf("api:default/analysis-http"),"group:default/analysis-control-team");
  assert.ok(catalog.consumersOf("api:default/analysis-http").includes("component:default/analysis-api-platform"));
});

test("orphan API rejected", () => {
  const records = structuredClone(load("catalog/entities.json").entities);
  records.push({kind:"API",namespace:"default",name:"orphan",owner:"group:default/api-platform-team",lifecycle:"active",system:"system:default/analysis-platform"});
  assert.throws(() => new Catalog(records),/orphan-api/);
});

test("registry immutability", () => {
  const registry = new ContractRegistry();
  const record = {apiRef:"api:default/x",protocol:"openapi",version:"1.0.0",source:"x",lifecycle:"active",owner:"group:default/x",compatibilityEvidence:"e.json",publishedAt:"2026-08-08T00:00:00Z"};
  assert.equal(registry.publish(record,Buffer.from("a")),"published");
  assert.equal(registry.publish(record,Buffer.from("a")),"idempotent");
  assert.throws(() => registry.publish(record,Buffer.from("b")),/immutable-release/);
});

test("blocker cannot be averaged away", () => {
  assert.equal(evaluateFindings([{ruleId:"SEC-001",severity:"blocker",status:"fail",entityRef:"api:default/x",message:"missing"},{ruleId:"DOC-001",severity:"major",status:"pass",entityRef:"api:default/x",message:"ok"}]),"fail");
});

test("exception requires expiry", () => {
  const record = load("governance/exceptions.json").exceptions[0];
  assert.deepEqual(validateException(record,new Date("2026-08-08T00:00:00Z")),[true,"valid"]);
  delete record.expiresAt;
  assert.equal(validateException(record,new Date("2026-08-08T00:00:00Z"))[0],false);
});

test("retirement blocked by consumer", () => {
  const policy = load("lifecycle/policy.json");
  const result = evaluateTransition({current:"deprecated",target:"retired",evidence:["zeroBlockingConsumers","retirementApproval","runtimeRemovalPlan","archivePlan"],policy,blockingConsumers:1});
  assert.deepEqual(result,{allowed:false,reason:"blocking-consumers"});
});

test("deprecation impact", () => {
  const result = deprecationImpact(load("lifecycle/consumers.json").consumers,"api:default/analysis-http","1.1.0");
  assert.equal(result.retirementDecision,"blocked");
  assert.deepEqual(result.blockingConsumers,["consumer-legacy-cli"]);
});

test("template parameter and secret checks", () => {
  const spec=load("templates/api-capability/template.json");
  const params={api_name:"reporting-api",title:"Reporting API",owner:"group:default/analysis-control-team",protocol:"openapi",system:"system:default/analysis-platform"};
  validateParameters(params,spec);
  assert.equal(renderText("# {{title}}",params),"# Reporting API");
  assert.throws(() => renderText("token=abcdefghijk",params),/embedded-secret/);
});

test("sandbox isolation", () => {
  const profile=load("sandbox/profile.json"); const session=createSession("learner","1",new Date("2026-08-08T00:00:00Z"),profile);
  assert.ok(session.tenant.startsWith("sandbox-"));
  assert.throws(() => validateImport("production"),/production-data-forbidden/);
});

test("runtime drift and ownership boundary", () => {
  const desired=load("runtime/desired-routes.json").routes; const current=load("runtime/current-routes.json").routes;
  assert.equal(routeDrift(desired,current).inSync,true);
  desired.forEach(validateRoute);
  assert.throws(() => validateRoute({...desired[0],domainAuthz:"gateway-project-owner"}),/domain-policy-at-edge/);
});

test("outcome analytics", () => {
  const events=fs.readFileSync(path.join(cap,"analytics/usage-events.jsonl"),"utf8").trim().split("\n").map(JSON.parse);
  assert.deepEqual(productMetrics(events,new Set(["api:default/analysis-http@1.1.0"])),{activeConsumers:5,medianTimeToFirstSuccessSeconds:240,deprecatedVersionUses:1});
});

test("scorecards expose blockers", () => {
  const evidence=load("governance/evidence-ledger.json").evidence;
  assert.equal(scorecard("api:default/analysis-http",evidence).status,"ready");
  evidence.push({entityRef:"api:default/analysis-http",kind:"security",status:"fail"});
  assert.equal(scorecard("api:default/analysis-http",evidence).status,"blocked");
});

test("release gate", () => {
  const base={catalogValid:true,registryValid:true,policyDecision:"pass",lifecycleSafe:true,templateSafe:true,docsComplete:true,sdkTraceable:true,runtimeSafe:true,sandboxSafe:true};
  assert.equal(evaluatePlatformRelease(base).decision,"accepted");
  assert.deepEqual(evaluatePlatformRelease({...base,runtimeSafe:false}),{decision:"rejected",reasons:["runtime"]});
});
