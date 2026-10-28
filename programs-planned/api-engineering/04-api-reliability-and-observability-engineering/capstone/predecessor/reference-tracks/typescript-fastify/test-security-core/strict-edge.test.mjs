import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { parseStrictJson } from "../dist-security/security/strict-json.js";
import { evaluateEdge } from "../dist-security/security/edge.js";

const vectors = new URL("../../../../shared/vectors/", import.meta.url);
const load = async (name) => JSON.parse(await readFile(new URL(name, vectors), "utf8"));

test("strict JSON shared vectors", async () => {
  const data = await load("strict-json.json");
  for (const item of data.cases) {
    if (item.valid) assert.doesNotThrow(() => parseStrictJson(item.text, 1_048_576, item.maxDepth ?? 32), item.id);
    else assert.throws(() => parseStrictJson(item.text, 1_048_576, item.maxDepth ?? 32), (error) => error.code === item.error, item.id);
  }
});

test("edge shared vectors", async () => {
  const data = await load("edge.json");
  for (const item of data.cases) {
    const input = { peer:item.peer, headers:item.headers, trustedProxies:item.trustedProxies ?? [], allowedHosts:item.allowedHosts ?? ["api.example.test"] };
    if (item.valid) assert.equal(evaluateEdge(input).origin, item.origin, item.id);
    else assert.throws(() => evaluateEdge(input), (error) => error.code === item.error, item.id);
  }
});
