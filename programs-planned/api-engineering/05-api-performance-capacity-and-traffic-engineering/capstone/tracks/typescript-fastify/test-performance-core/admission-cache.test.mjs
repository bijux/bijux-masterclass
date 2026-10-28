import test from "node:test";
import assert from "node:assert/strict";

import {
  AdmissionRejected,
  FairAdmission,
} from "../dist/performance/admission.js";
import {
  BoundedTTLCache,
  createAuthorizedCacheKey,
} from "../dist/performance/cache.js";
import {
  SingleFlight,
  SingleFlightRejected,
} from "../dist/performance/singleflight.js";

const key = (tenant = "t1", version = "1", resourceId = "p1") =>
  createAuthorizedCacheKey({
    tenantId: tenant,
    policyPartition: "owner",
    resourceType: "project",
    resourceId,
    version,
    representation: "api-1.2",
  });

test("admission enforces global and per-key limits", async () => {
  const admission = new FairAdmission(2, 2, 1);
  const a = await admission.acquire("a");
  const b = await admission.acquire("b");
  assert.equal(admission.snapshot().active, 2);
  await assert.rejects(admission.acquire("a", 5), AdmissionRejected);
  a.release();
  b.release();
  assert.equal(admission.snapshot().active, 0);
  assert.throws(() => a.release());
});

test("waiter capacity is bounded", async () => {
  const admission = new FairAdmission(1, 1, 1);
  const first = await admission.acquire("a");
  const waiting = admission.acquire("b");
  await assert.rejects(admission.acquire("c"), /waiter-capacity/);
  first.release();
  const second = await waiting;
  second.release();
});

test("authorized cache key partitions tenants and versions", () => {
  assert.notEqual(key("a").canonical, key("b").canonical);
  assert.notEqual(key("a", "1").canonical, key("a", "2").canonical);
});

test("bounded TTL cache expires and evicts", () => {
  const cache = new BoundedTTLCache(2, 100n);
  cache.put(key(), "a", { nowNs: 0n, ttlNs: 10n, sizeBytes: 10n });
  assert.equal(cache.get(key(), 5n).state, "hit");
  assert.equal(cache.get(key(), 10n).state, "stale");
  cache.put(key("t1", "1", "p1"), "a", { nowNs: 0n, ttlNs: 100n, sizeBytes: 10n });
  cache.put(key("t1", "1", "p2"), "b", { nowNs: 0n, ttlNs: 100n, sizeBytes: 10n });
  cache.put(key("t1", "1", "p3"), "c", { nowNs: 0n, ttlNs: 100n, sizeBytes: 10n });
  assert.equal(cache.snapshot().entries, 2);
  assert.equal(cache.snapshot().evictions, 1);
});

test("single-flight makes one origin call", async () => {
  const flight = new SingleFlight(2, 20);
  let calls = 0;
  const origin = async () => {
    calls += 1;
    await new Promise((resolve) => setTimeout(resolve, 5));
    return 7;
  };
  const values = await Promise.all(
    Array.from({ length: 10 }, () => flight.do("key", origin)),
  );
  assert.deepEqual(values, Array(10).fill(7));
  assert.equal(calls, 1);
  assert.equal(flight.snapshot().fills, 0);
});

test("single-flight fill capacity is bounded", async () => {
  const flight = new SingleFlight(1, 2);
  let release;
  const blocked = new Promise((resolve) => {
    release = resolve;
  });
  const first = flight.do("a", async () => {
    await blocked;
    return 1;
  });
  await new Promise((resolve) => setTimeout(resolve, 0));
  await assert.rejects(flight.do("b", async () => 2), SingleFlightRejected);
  release();
  assert.equal(await first, 1);
});
