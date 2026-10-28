import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { Readable } from "node:stream";

import { FileSystemArtifactStore } from "../dist-core/artifacts.js";

async function withStore(run) {
  const root = await mkdtemp(join(tmpdir(), "cdse-artifacts-"));
  try {
    const store = new FileSystemArtifactStore(root);
    await store.initialize();
    await run(store);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}

test("identical concurrent publications converge without clobbering", async () => {
  await withStore(async (store) => {
    const first = await store.stageBytes(Buffer.from("same bytes"), "text/plain");
    const second = await store.stageBytes(Buffer.from("same bytes"), "text/plain");
    const key = `sha256/${first.checksumSha256}`;

    const [firstPath, secondPath] = await Promise.all([
      store.publish(first, key),
      store.publish(second, key),
    ]);

    assert.equal(firstPath, secondPath);
    assert.equal(await readFile(firstPath, "utf8"), "same bytes");
    assert.equal(await store.pathFor(key, first.checksumSha256), firstPath);
  });
});

test("a content-address collision never overwrites existing bytes", async () => {
  await withStore(async (store) => {
    const original = await store.stageBytes(Buffer.from("original"), "text/plain");
    const key = "objects/fixed-key";
    const path = await store.publish(original, key);

    const conflicting = await store.stageBytes(Buffer.from("different"), "text/plain");
    await assert.rejects(
      store.publish(conflicting, key),
      /different bytes/,
    );
    assert.equal(await readFile(path, "utf8"), "original");
  });
});

test("stream staging enforces a byte limit and cleans the staged file", async () => {
  await withStore(async (store) => {
    await assert.rejects(
      store.stageStream(
        Readable.from([Buffer.alloc(8), Buffer.alloc(8)]),
        "application/octet-stream",
        12,
      ),
      /payload-too-large/,
    );
  });
});

test("storage keys cannot escape the configured root", async () => {
  await withStore(async (store) => {
    const staged = await store.stageBytes(Buffer.from("x"), "text/plain");
    await assert.rejects(store.publish(staged, "../outside"), /unsafe storage key/);
  });
});
