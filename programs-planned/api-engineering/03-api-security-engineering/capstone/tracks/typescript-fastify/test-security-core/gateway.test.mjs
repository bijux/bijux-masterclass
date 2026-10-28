import test from "node:test";
import assert from "node:assert/strict";
import { authenticateExactlyOne, securityDecision } from "../dist-security/security/gateway.js";

const principal={subject:"u1",tenant:"t1",scopes:new Set(["projects:read"]),roles:new Set(),assurance:"baseline",authAgeSeconds:0};
const validator=()=>principal;

test("exactly one credential and integrated policy",()=>{
  assert.equal(authenticateExactlyOne({bearerToken:"x"},validator,validator),principal);
  assert.throws(()=>authenticateExactlyOne({},validator,validator),(e)=>e.code==="credential-required");
  assert.throws(()=>authenticateExactlyOne({bearerToken:"x",apiKey:"y"},validator,validator),(e)=>e.code==="credential-ambiguous");
  const policies=new Map([["getProject",{operationId:"getProject",scopes:new Set(["projects:read"]),roles:new Set(),relationship:"owner",tenantBound:true,conceal:true,requiredAssurance:"baseline"}]]);
  const allowed=securityDecision({operationId:"getProject",credentials:{bearerToken:"x"},resource:{tenant:"t1",owner:"u1",members:new Set()},policies,bearerValidator:validator,apiKeyValidator:validator});
  assert.equal(allowed.decision.allowed,true);
  const denied=securityDecision({operationId:"getProject",credentials:{bearerToken:"x"},resource:{tenant:"t2",owner:"u2",members:new Set()},policies,bearerValidator:validator,apiKeyValidator:validator});
  assert.equal(denied.decision.allowed,false); assert.equal(denied.decision.conceal,true);
});
