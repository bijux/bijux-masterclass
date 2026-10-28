import test from "node:test";
import assert from "node:assert/strict";

import {
  canonicalWebhookBody,
  validateDestination,
  webhookSignature,
} from "../dist-core/webhooks.js";

test("approved webhook destinations retain path and query", () => {
  const url = validateDestination(
    "https://hooks.example.test:443/analysis-complete?tenant=learner",
  );
  assert.equal(url.hostname, "hooks.example.test");
  assert.equal(url.pathname, "/analysis-complete");
  assert.equal(url.search, "?tenant=learner");
});

for (const value of [
  "http://hooks.example.test/path",
  "https://user@hooks.example.test/path",
  "https://hooks.example.test:444/path",
  "https://hooks.example.test/path#fragment",
  "https://evil.example.test/path",
]) {
  test(`rejects unsafe webhook destination: ${value}`, () => {
    assert.throws(() => validateDestination(value));
  });
}

test("canonical body and signature use the shared byte-level profile", () => {
  const body = canonicalWebhookBody({ b: 2, a: 1 });
  assert.equal(body.toString("utf8"), '{"a":1,"b":2}');
  assert.match(
    webhookSignature("secret-value", "1722859200", body),
    /^sha256=[a-f0-9]{64}$/,
  );
});
