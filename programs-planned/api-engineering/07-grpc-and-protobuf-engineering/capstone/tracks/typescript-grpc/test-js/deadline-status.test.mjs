import test from "node:test";
import assert from "node:assert/strict";
import { Deadline, retryAllowed, retryDelay } from "../dist/src/deadline.js";
import { safeDetail, statusFor } from "../dist/src/status.js";

class Clock {
  value = 0;
  nowSeconds() { return this.value; }
}

test("child timeout uses remaining absolute budget", () => {
  const clock = new Clock();
  const deadline = Deadline.after(5, clock);
  clock.value = 2;
  assert.equal(deadline.childTimeout(0.5, 10), 2.5);
});

test("retry requires idempotency for mutation", () => {
  const policy = {
    maxAttempts:3, initialBackoff:0.1, multiplier:2, maxBackoff:1,
    retryableStatuses:new Set(["UNAVAILABLE"]),
  };
  assert.equal(retryAllowed({
    policy, method:"CreateRun", status:"UNAVAILABLE", attempt:1,
    idempotent:false, remaining:2, nextDelay:0.1,
  }), false);
  assert.equal(retryAllowed({
    policy, method:"CreateRun", status:"UNAVAILABLE", attempt:1,
    idempotent:true, remaining:2, nextDelay:0.1,
  }), true);
});

test("retry delay is bounded", () => {
  const policy = {
    maxAttempts:5, initialBackoff:1, multiplier:2, maxBackoff:5,
    retryableStatuses:new Set(["UNAVAILABLE"]),
  };
  assert.equal(retryDelay(policy, 5, 1), 5);
  assert.equal(retryDelay(policy, 1, 0.25), 0.5);
});

test("status mapping is stable and safe", () => {
  assert.equal(statusFor({kind:"conflict"}), "ABORTED");
  assert.deepEqual(
    safeDetail({kind:"invalid", field:"algorithm"}),
    {reason:"invalid", field:"algorithm"},
  );
});
