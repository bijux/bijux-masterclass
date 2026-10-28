import test from "node:test";
import assert from "node:assert/strict";

import {
  canonicalJson,
  evolve,
  parseCursor,
  parseProjectEtag,
  projectEtag,
  retryDelaySeconds,
} from "../dist-core/domain.js";

test("canonical JSON is deterministic", () => {
  assert.equal(canonicalJson({ b: 2, a: [2, 1] }), '{"a":[2,1],"b":2}');
});

test("entity tags round-trip", () => {
  assert.equal(parseProjectEtag(projectEtag("prj_0001", 7), "prj_0001"), 7);
});

test("cursor handles retain bigint precision as strings", () => {
  assert.equal(parseCursor("9223372036854775807"), "9223372036854775807");
  assert.throws(() => parseCursor("9223372036854775808"));
  assert.throws(() => parseCursor("0"));
});

test("cancellation is requested before it is observed", () => {
  const requested = evolve(
    { state: "running", progress: 40, cancellationRequested: false },
    "request-cancel",
  );
  assert.equal(requested.state, "running");
  assert.equal(evolve(requested, "observe-cancel").state, "canceled");
});

test("retry delay is bounded", () => {
  assert.equal(retryDelaySeconds(99), 300);
});

test("canonical JSON rejects cross-language number ambiguity", () => {
  assert.throws(() => canonicalJson({ value: 1.5 }));
  assert.throws(() => canonicalJson({ value: 9_007_199_254_740_992 }));
});

test("canonical JSON sorts Unicode names by code point", () => {
  assert.equal(canonicalJson({ "😀": 1, "￿": 2 }), '{"￿":2,"😀":1}');
});
