import test from "node:test";
import assert from "node:assert/strict";
import { Deadline, DeadlineExceeded, ManualClock, formatTraceparent, parseTraceparent } from "../dist-reliability/context-entry.js";

test("traceparent round trip", () => {
  const value = "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01";
  assert.equal(formatTraceparent(parseTraceparent(value)), value);
});

test("child deadline cannot extend parent", () => {
  const clock = new ManualClock(1000); const parent = Deadline.after(clock, 500); const child = parent.child(clock, 2000);
  assert.equal(child.expiresAtMs, parent.expiresAtMs); clock.advance(500); assert.throws(() => child.requireRemaining(clock), DeadlineExceeded);
});
