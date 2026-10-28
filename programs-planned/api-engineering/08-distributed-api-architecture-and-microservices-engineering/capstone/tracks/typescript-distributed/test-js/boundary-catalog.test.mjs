import assert from "node:assert/strict";
import test from "node:test";

import { boundaryDecision } from "../dist/src/boundary.js";
import { ServiceCatalog } from "../dist/src/catalog.js";


test("boundary evidence approves an autonomous capability", () => {
  const decision = boundaryDecision({
    name: "notification",
    ownership: 2,
    dataAutonomy: 2,
    changeIndependence: 2,
    scaleIsolation: 1,
    failureIsolation: 2,
    securityBoundary: 1,
    operationalCost: 1,
    synchronousCoupling: 0,
  });
  assert.equal(decision, "extract");
});


test("boundary evidence rejects table-per-service decomposition", () => {
  const decision = boundaryDecision({
    name: "table",
    ownership: 1,
    dataAutonomy: 0,
    changeIndependence: 0,
    scaleIsolation: 0,
    failureIsolation: 0,
    securityBoundary: 0,
    operationalCost: 1,
    synchronousCoupling: 2,
  });
  assert.equal(decision, "reject");
});


test("service catalog enforces one writer per fact", () => {
  const catalog = new ServiceCatalog();
  catalog.add({
    name: "control",
    owner: "team-control",
    kind: "business",
    dataFacts: new Set(["run"]),
    interfaces: new Set(),
  });
  catalog.add({
    name: "artifact",
    owner: "team-artifact",
    kind: "business",
    dataFacts: new Set(["artifact"]),
    interfaces: new Set(),
  });
  catalog.validateSingleWriters();
  assert.equal(catalog.ownerOf("artifact"), "artifact");
});


test("duplicate writers are rejected", () => {
  const catalog = new ServiceCatalog();
  catalog.add({
    name: "a",
    owner: "team-a",
    kind: "business",
    dataFacts: new Set(["run"]),
    interfaces: new Set(),
  });
  catalog.add({
    name: "b",
    owner: "team-b",
    kind: "business",
    dataFacts: new Set(["run"]),
    interfaces: new Set(),
  });
  assert.throws(() => catalog.validateSingleWriters());
});
