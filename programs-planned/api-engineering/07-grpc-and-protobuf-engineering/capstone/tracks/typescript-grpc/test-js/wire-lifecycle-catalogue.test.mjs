import test from "node:test";
import assert from "node:assert/strict";
import { concat, decodeVarint, encodeInt64Field, encodeStringField, encodeVarint } from "../dist/src/wire.js";
import { Lifecycle } from "../dist/src/lifecycle.js";
import { METHODS, validateCatalogue } from "../dist/src/catalogue.js";

test("varint round trips 64-bit boundary", () => {
  const value = 9223372036854775807n;
  const bytes = encodeVarint(value);
  assert.equal(decodeVarint(bytes).value, value);
});

test("wire field helpers emit nonempty deterministic bytes", () => {
  const bytes = concat(encodeStringField(1, "run"), encodeInt64Field(9, 9007199254740992n));
  assert.ok(bytes.length > 5);
  assert.deepEqual(Array.from(bytes), Array.from(concat(encodeStringField(1, "run"), encodeInt64Field(9, 9007199254740992n))));
});

test("lifecycle stops admission during drain", () => {
  const lifecycle = new Lifecycle();
  lifecycle.start();
  const release = lifecycle.admit();
  lifecycle.drain();
  assert.equal(lifecycle.serving(), false);
  assert.throws(() => lifecycle.admit());
  lifecycle.stop();
  assert.equal(lifecycle.phase(), "stopping");
  release();
  assert.equal(lifecycle.phase(), "stopped");
});

test("catalogue contains seven unique governed methods", () => {
  validateCatalogue();
  assert.equal(METHODS.length, 7);
  assert.equal(new Set(METHODS.map(m => m.path)).size, 7);
  assert.ok(METHODS.some(m => m.shape === "bidi-stream"));
});
