import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { CapabilityAuthority } from "../dist/src/capability.js";
import { ArtifactCompletionSaga } from "../dist/src/saga.js";


const claims = {
  jti: "j",
  issuer: "control",
  audience: "artifact-service",
  subject: "u",
  tenant: "t",
  resource: "r",
  action: "artifact:upload",
  issuedAt: 10,
  expiresAt: 20,
  sha256: "abc",
  maxBytes: 10,
};


test("capability is audience, tenant, action, and time bound", () => {
  const authority = new CapabilityAuthority(
    "control",
    "0123456789abcdef0123456789abcdef",
  );
  const token = authority.mint(claims);
  const verified = authority.verify(token, {
    audience: "artifact-service",
    tenant: "t",
    action: "artifact:upload",
    now: 11,
  });
  assert.equal(verified.resource, "r");
  assert.throws(() => authority.verify(token, {
    audience: "control",
    tenant: "t",
    action: "artifact:upload",
    now: 11,
  }));
  assert.throws(() => authority.verify(token, {
    audience: "artifact-service",
    tenant: "t",
    action: "artifact:upload",
    now: 21,
  }));
});


test("TypeScript matches the cross-language golden token", () => {
  const vectorUrl = new URL(
    "./fixtures/capability.json",
    import.meta.url,
  );
  const vector = JSON.parse(readFileSync(vectorUrl, "utf8")).interoperability;
  const wire = vector.claims;
  const authority = new CapabilityAuthority(
    wire.issuer,
    vector.key_utf8,
  );
  const token = authority.mint({
    jti: wire.jti,
    issuer: wire.issuer,
    audience: wire.audience,
    subject: wire.subject,
    tenant: wire.tenant,
    resource: wire.resource,
    action: wire.action,
    issuedAt: wire.issued_at,
    expiresAt: wire.expires_at,
    sha256: wire.sha256,
    maxBytes: wire.max_bytes,
  });
  assert.equal(token, vector.expected_token);
});


test("saga is idempotent and compensates stale attempts", () => {
  const saga = new ArtifactCompletionSaga("s", "r", "a");
  assert.equal(saga.recordArtifact("e", "x", "a"), "stored");
  assert.equal(saga.recordArtifact("e", "x", "a"), "duplicate");
  assert.equal(saga.complete("c", "a"), "completed");

  const stale = new ArtifactCompletionSaga("s2", "r", "a");
  assert.equal(stale.recordArtifact("e", "x", "old"), "compensate");
  assert.equal(stale.compensate("k"), "compensated");
});
