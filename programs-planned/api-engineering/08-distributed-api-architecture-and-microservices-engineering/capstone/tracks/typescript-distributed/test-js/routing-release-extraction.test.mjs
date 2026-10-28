import assert from "node:assert/strict";
import test from "node:test";

import { StranglerRouter } from "../dist/src/extraction.js";
import { VersionPolicy } from "../dist/src/release.js";
import { ServiceRegistry } from "../dist/src/routing.js";


test("registry routes only to healthy accepting instances", () => {
  const registry = new ServiceRegistry();
  registry.register({
    instanceId: "a",
    service: "control",
    version: "1.0",
    healthy: true,
    accepting: true,
  });
  registry.register({
    instanceId: "b",
    service: "control",
    version: "1.0",
    healthy: true,
    accepting: true,
  });
  assert.deepEqual(
    [
      registry.choose("control").instanceId,
      registry.choose("control").instanceId,
      registry.choose("control").instanceId,
    ],
    ["a", "b", "a"],
  );
  registry.setHealth("control", "a", false);
  assert.equal(registry.choose("control").instanceId, "b");
});


test("version skew policy is bounded", () => {
  const policy = new VersionPolicy();
  assert.equal(policy.classify("1.0", "1.1"), "compatible");
  assert.equal(
    policy.classify("1.1", "1.0"),
    "compatible-with-feature-disabled",
  );
  assert.equal(policy.classify("2.0", "1.0"), "reject");
});


test("shadow divergence blocks promotion", () => {
  const router = new StranglerRouter(
    (value) => value,
    (value) => value + 1,
  );
  router.transition("shadow");
  assert.equal(router.call("k", 1), 1);
  assert.equal(router.shadowClean(), false);
  assert.throws(() => router.transition("canary", 0.1));
});


test("clean shadow progresses through canary before cutover", () => {
  const router = new StranglerRouter(
    (value) => value * 2,
    (value) => value * 2,
  );
  router.transition("shadow");
  router.call("k", 2);
  assert.equal(router.shadowClean(), true);
  assert.throws(() => router.transition("cutover"));
  router.transition("canary", 0.5);
  router.transition("cutover");
  assert.equal(router.call("k", 3), 6);
});
