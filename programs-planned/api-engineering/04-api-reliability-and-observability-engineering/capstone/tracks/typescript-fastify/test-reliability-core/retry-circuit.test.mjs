import test from "node:test";
import assert from "node:assert/strict";
import { CircuitBreaker, CircuitOpen, ManualClock, planRetryDelays, retryable } from "../dist-reliability/index.js";

test("retry classification protects unsafe operations", () => {
  assert.equal(retryable({ status: 503, transportError: false, safety: "unsafe" }), false);
  assert.equal(retryable({ status: 503, transportError: false, safety: "idempotent" }), true);
});

test("deterministic jitter schedule", () => {
  assert.deepEqual(planRetryDelays({ maxAttempts: 4, initialDelayMs: 100, maximumDelayMs: 1000, multiplier: 2, jitter: "full" }, 7), [24, 183, 245]);
});

test("circuit opens and recovers through one half-open probe", () => {
  const clock = new ManualClock(); const circuit = new CircuitBreaker(2, 100);
  circuit.allow(clock); circuit.failure(clock); circuit.allow(clock); circuit.failure(clock);
  assert.equal(circuit.state, "open"); assert.throws(() => circuit.allow(clock), CircuitOpen);
  clock.advance(100); circuit.allow(clock); assert.equal(circuit.state, "half-open"); circuit.success(); assert.equal(circuit.state, "closed");
});
