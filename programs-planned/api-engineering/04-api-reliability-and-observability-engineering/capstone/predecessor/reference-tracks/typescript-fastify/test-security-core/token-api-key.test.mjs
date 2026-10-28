import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { validateAccessToken } from "../dist-security/security/tokens.js";
import { SecretBytes } from "../dist-security/security/secrets.js";
import { digestApiKey, verifyApiKey } from "../dist-security/security/api-keys.js";

const identity = new URL("../../../../identity-provider/", import.meta.url);
const profile = { issuer:"https://issuer.security.test", audience:"analysis-runs-api", algorithms:["RS256"], tokenType:"at+jwt", clockSkewSeconds:30, maxLifetimeSeconds:900, requiredClaims:["iss","aud","sub","exp","iat","jti","tenant","scope"] };
const neverRevoked = { isRevoked(){ return false; } };

test("JWT validation profile", async () => {
  const jwks=JSON.parse(await readFile(new URL("jwks.json",identity),"utf8"));
  const tokens=JSON.parse(await readFile(new URL("tokens.json",identity),"utf8"));
  const principal=validateAccessToken({token:tokens.valid,profile,jwks,now:tokens.now+1,revocations:neverRevoked});
  assert.equal(principal.subject,"user-01"); assert(principal.scopes.has("runs:write"));
  for(const key of ["wrongAudience","wrongIssuer","tooLong"]) assert.throws(()=>validateAccessToken({token:tokens[key],profile,jwks,now:tokens.now+1,revocations:neverRevoked}),undefined,key);
  assert.throws(()=>validateAccessToken({token:tokens.revoked,profile,jwks,now:tokens.now+1,revocations:{isRevoked(_i,j){return j==="revoked-jti";}}}));
});

test("API key peppered digest", () => {
  const pepper=new SecretBytes("fixture-pepper"); const raw="ak_key01.high-entropy-fixture-secret";
  const record={keyId:"key01",owner:"user-01",tenant:"tenant-01",digestHex:digestApiKey(raw,pepper),scopes:["projects:read"]};
  const principal=verifyApiKey(raw,new Map([["key01",record]]),pepper,100);
  assert.equal(principal.subject,"user-01");
  assert.throws(()=>verifyApiKey("ak_key01.wrong",new Map([["key01",record]]),pepper,100));
});
