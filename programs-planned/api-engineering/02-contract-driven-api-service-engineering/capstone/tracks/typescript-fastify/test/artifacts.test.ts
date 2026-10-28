import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { Readable } from "node:stream";

import { describe, expect, it } from "vitest";

import { FileSystemArtifactStore } from "../src/artifacts.js";

describe("filesystem artifact adapter", () => {
  it("stages incrementally and publishes by checksum", async () => {
    const root = await mkdtemp(join(tmpdir(), "cdse-artifacts-"));
    const store = new FileSystemArtifactStore(root);
    const staged = await store.stageStream(
      Readable.from([Buffer.from("alpha"), Buffer.from("beta")]),
      "text/plain",
      100,
    );
    const key = `objects/${staged.checksumSha256}`;
    const path = await store.publish(staged, key);
    expect((await readFile(path)).toString()).toBe("alphabeta");
    await expect(store.pathFor(key, staged.checksumSha256)).resolves.toBe(path);
  });

  it("publishes identical concurrent content exactly once", async () => {
    const root = await mkdtemp(join(tmpdir(), "cdse-artifacts-"));
    const store = new FileSystemArtifactStore(root);
    const staged = await Promise.all(
      Array.from({ length: 16 }, () =>
        store.stageBytes(Buffer.from("same bytes"), "text/plain"),
      ),
    );
    const key = `objects/${staged[0]!.checksumSha256}`;
    const paths = await Promise.all(
      staged.map((value) => store.publish(value, key)),
    );
    expect(new Set(paths).size).toBe(1);
    expect((await readFile(paths[0]!)).toString()).toBe("same bytes");
  });

  it("refuses a content-address collision", async () => {
    const root = await mkdtemp(join(tmpdir(), "cdse-artifacts-"));
    const store = new FileSystemArtifactStore(root);
    const first = await store.stageBytes(Buffer.from("first"), "text/plain");
    await store.publish(first, "objects/fixed");
    const second = await store.stageBytes(Buffer.from("second"), "text/plain");
    await expect(store.publish(second, "objects/fixed")).rejects.toThrow(
      "different bytes",
    );
  });

  it("rejects traversal", async () => {
    const root = await mkdtemp(join(tmpdir(), "cdse-artifacts-"));
    const store = new FileSystemArtifactStore(root);
    await expect(store.pathFor("../secret")).rejects.toThrow();
  });

  it("detects changed bytes", async () => {
    const root = await mkdtemp(join(tmpdir(), "cdse-artifacts-"));
    const store = new FileSystemArtifactStore(root);
    const staged = await store.stageBytes(Buffer.from("original"), "text/plain");
    const path = await store.publish(staged, "objects/value");
    await writeFile(path, "tampered");
    await expect(
      store.pathFor("objects/value", staged.checksumSha256),
    ).rejects.toThrow("integrity");
  });
});
