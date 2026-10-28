import assert from "node:assert/strict";
import test from "node:test";

import { VersionedProjection } from "../dist/src/consistency.js";
import {
  DependencyGraph,
  serialAvailability,
} from "../dist/src/topology.js";


test("dependency graph detects cycles and enforces public depth", () => {
  const graph = new DependencyGraph([
    {
      source: "edge-gateway",
      target: "control",
      purpose: "query",
      budgetMs: 100,
    },
    {
      source: "control",
      target: "artifact",
      purpose: "lookup",
      budgetMs: 100,
    },
  ]);
  assert.equal(graph.longestDepth("edge-gateway"), 2);
  graph.validate(2, new Set());

  const cycle = new DependencyGraph([
    { source: "a", target: "b", purpose: "x", budgetMs: 1 },
    { source: "b", target: "a", purpose: "y", budgetMs: 1 },
  ]);
  assert.ok(cycle.cycle());
  assert.throws(() => cycle.validate(2, new Set()));
});


test("serial availability compounds across mandatory dependencies", () => {
  assert.ok(Math.abs(serialAvailability([0.99, 0.99, 0.99]) - 0.970299) < 1e-12);
});


test("versioned projection distinguishes duplicate, stale, and gap", () => {
  const projection = new VersionedProjection();
  assert.equal(projection.apply("r", 1, { state: "queued" }, 0), "apply");
  assert.equal(projection.apply("r", 1, { state: "queued" }, 1), "duplicate");
  assert.equal(projection.apply("r", 2, { state: "running" }, 2), "apply");
  assert.equal(projection.apply("r", 1, { state: "old" }, 3), "stale");
  assert.equal(projection.apply("r", 4, { state: "done" }, 4), "gap");
});
