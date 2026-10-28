import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { BoundedQueue, parseUpload, WatchCursor, WorkerProtocol } from "../dist/src/stream.js";
import { authenticate, requireScope, requireTenant } from "../dist/src/security.js";

const body = new TextEncoder().encode("course-seven");
const digest = createHash("sha256").update(body).digest("hex");

test("upload requires metadata first and validates digest", () => {
  assert.throws(() => parseUpload([{kind:"chunk", data:body}]));
  const parsed = parseUpload([
    {kind:"metadata", parent:"projects/p-1", requestId:"u-1",
     filename:"x.bin", mediaType:"application/octet-stream",
     sha256:digest, expectedSize:BigInt(body.length)},
    {kind:"chunk", data:body},
  ]);
  assert.equal(parsed.sha256, digest);
});

test("bounded queue rejects overflow and records high water", () => {
  const queue = new BoundedQueue(2);
  queue.push(1); queue.push(2);
  assert.equal(queue.highWater, 2);
  assert.throws(() => queue.push(3), /queue full/);
});

test("watch cursor deduplicates and detects gaps", () => {
  const cursor = new WatchCursor(3n);
  assert.equal(cursor.accept(4n), "new");
  assert.equal(cursor.accept(4n), "duplicate");
  assert.throws(() => cursor.accept(6n), /gap/);
});

test("worker protocol requires exactly one hello first", () => {
  const protocol = new WorkerProtocol();
  assert.throws(() => protocol.accept({kind:"ready", availableSlots:1}));
  protocol.accept({kind:"hello", workerId:"worker-1", tenantId:"tenant-a", maxConcurrency:1});
  assert.equal(protocol.identity(), "worker-1");
  assert.throws(() => protocol.accept({kind:"hello", workerId:"worker-1", tenantId:"tenant-a", maxConcurrency:1}));
});

test("security rejects duplicate credentials and wrong tenant", () => {
  assert.throws(() => authenticate(["Bearer learner-write", "Bearer learner-read"]));
  const principal = authenticate(["Bearer learner-write"]);
  requireScope(principal, "runs:write");
  assert.throws(() => requireTenant(principal, "projects/p-b-1/runs/r-1"));
});
