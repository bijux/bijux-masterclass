import { createHash, randomUUID } from "node:crypto";
import { createReadStream, createWriteStream } from "node:fs";
import {
  link,
  lstat,
  mkdir,
  open,
  rm,
  stat,
  writeFile,
} from "node:fs/promises";
import { dirname, isAbsolute, relative, resolve, sep } from "node:path";
import { Readable, Transform } from "node:stream";
import { pipeline } from "node:stream/promises";

import type { StagedFile } from "./types.js";

const CHUNK_SIZE = 64 * 1024;

export class FileSystemArtifactStore {
  private readonly root: string;
  private readonly staging: string;

  public constructor(root: string) {
    this.root = resolve(root);
    this.staging = resolve(this.root, ".staging");
  }

  public async initialize(): Promise<void> {
    await mkdir(this.staging, { recursive: true });
  }

  private safe(key: string): string {
    if (
      isAbsolute(key) ||
      key.length === 0 ||
      key.split("/").includes("..") ||
      key.includes("\\")
    ) {
      throw new Error("unsafe storage key");
    }
    const path = resolve(this.root, key);
    const rel = relative(this.root, path);
    if (rel === ".." || rel.startsWith(`..${sep}`) || isAbsolute(rel)) {
      throw new Error("storage key escaped root");
    }
    return path;
  }

  public async stageStream(
    source: Readable,
    mediaType: string,
    limit: number,
  ): Promise<StagedFile> {
    await this.initialize();
    const temporaryPath = resolve(this.staging, `upload-${randomUUID()}`);
    const hash = createHash("sha256");
    let size = 0;

    const meter = new Transform({
      transform(chunk: Buffer, _encoding, callback) {
        size += chunk.length;
        if (size > limit) {
          callback(new Error("payload-too-large"));
          return;
        }
        hash.update(chunk);
        callback(null, chunk);
      },
    });

    try {
      await pipeline(
        source,
        meter,
        createWriteStream(temporaryPath, {
          flags: "wx",
          highWaterMark: CHUNK_SIZE,
        }),
      );
      if (size === 0) throw new Error("empty-upload");
      const handle = await open(temporaryPath, "r");
      try {
        await handle.sync();
      } finally {
        await handle.close();
      }
      return {
        temporaryPath,
        size,
        checksumSha256: hash.digest("hex"),
        mediaType,
      };
    } catch (error) {
      await rm(temporaryPath, { force: true });
      throw error;
    }
  }

  public async stageBytes(
    content: Uint8Array,
    mediaType: string,
  ): Promise<StagedFile> {
    if (content.byteLength === 0) throw new Error("artifact cannot be empty");
    await this.initialize();
    const temporaryPath = resolve(this.staging, `artifact-${randomUUID()}`);
    try {
      await writeFile(temporaryPath, content, { flag: "wx" });
      const handle = await open(temporaryPath, "r");
      try {
        await handle.sync();
      } finally {
        await handle.close();
      }
      return {
        temporaryPath,
        size: content.byteLength,
        checksumSha256: createHash("sha256").update(content).digest("hex"),
        mediaType,
      };
    } catch (error) {
      await rm(temporaryPath, { force: true });
      throw error;
    }
  }

  public async publish(staged: StagedFile, key: string): Promise<string> {
    const finalPath = this.safe(key);
    await mkdir(dirname(finalPath), { recursive: true });

    try {
      await link(staged.temporaryPath, finalPath);
      await this.syncDirectory(dirname(finalPath));
    } catch (error) {
      if (!isFileExistsError(error)) throw error;
      if (await this.isSymbolicLink(finalPath)) {
        throw new Error("refusing to publish through a symbolic link");
      }
      const existingDigest = await this.digest(finalPath);
      if (existingDigest !== staged.checksumSha256) {
        throw new Error("idempotent publish found different bytes");
      }
    } finally {
      await rm(staged.temporaryPath, { force: true });
    }
    return finalPath;
  }

  public async pathFor(
    key: string,
    expectedChecksum?: string,
  ): Promise<string> {
    const path = this.safe(key);
    if (await this.isSymbolicLink(path)) throw new Error("symbolic-link object");
    const metadata = await stat(path);
    if (!metadata.isFile()) throw new Error("artifact not found");
    if (expectedChecksum && (await this.digest(path)) !== expectedChecksum) {
      throw new Error("artifact integrity verification failed");
    }
    return path;
  }

  private async digest(path: string): Promise<string> {
    const hash = createHash("sha256");
    for await (const chunk of createReadStream(path, {
      highWaterMark: 128 * 1024,
    })) {
      hash.update(chunk as Buffer);
    }
    return hash.digest("hex");
  }

  private async isSymbolicLink(path: string): Promise<boolean> {
    try {
      return (await lstat(path)).isSymbolicLink();
    } catch (error) {
      if (isNotFoundError(error)) return false;
      throw error;
    }
  }

  private async syncDirectory(path: string): Promise<void> {
    const handle = await open(path, "r");
    try {
      await handle.sync();
    } finally {
      await handle.close();
    }
  }
}

function isFileExistsError(error: unknown): boolean {
  return (
    error instanceof Error &&
    "code" in error &&
    (error as NodeJS.ErrnoException).code === "EEXIST"
  );
}

function isNotFoundError(error: unknown): boolean {
  return (
    error instanceof Error &&
    "code" in error &&
    (error as NodeJS.ErrnoException).code === "ENOENT"
  );
}
