import { createHash } from "node:crypto";

export type UploadFrame =
  | { kind: "metadata"; parent: string; requestId: string; filename: string;
      mediaType: string; sha256: string; expectedSize: bigint }
  | { kind: "chunk"; data: Uint8Array };

export interface UploadParsed {
  readonly metadata: Extract<UploadFrame, { kind: "metadata" }>;
  readonly chunks: readonly Uint8Array[];
  readonly size: bigint;
  readonly sha256: string;
}

export function parseUpload(
  frames: readonly UploadFrame[],
  limits = { maxChunkBytes: 64 * 1024, maxTotalBytes: 2 * 1024 * 1024 },
): UploadParsed {
  const first = frames[0];
  if (first === undefined || first.kind !== "metadata") {
    throw new Error("first upload frame must contain metadata");
  }
  const chunks: Uint8Array[] = [];
  let total = 0;
  for (const frame of frames.slice(1)) {
    if (frame.kind !== "chunk") throw new Error("metadata may appear only once");
    if (frame.data.byteLength > limits.maxChunkBytes) {
      throw new Error("chunk exceeds limit");
    }
    total += frame.data.byteLength;
    if (total > limits.maxTotalBytes) throw new Error("upload exceeds limit");
    chunks.push(frame.data);
  }
  if (first.expectedSize !== 0n && first.expectedSize !== BigInt(total)) {
    throw new Error("size mismatch");
  }
  const hash = createHash("sha256");
  for (const chunk of chunks) hash.update(chunk);
  const digest = hash.digest("hex");
  if (first.sha256 !== "" && first.sha256.toLowerCase() !== digest) {
    throw new Error("checksum mismatch");
  }
  return { metadata: first, chunks, size: BigInt(total), sha256: digest };
}

export class BoundedQueue<T> {
  private readonly entries: T[] = [];
  public highWater = 0;

  public constructor(public readonly capacity: number) {
    if (!Number.isSafeInteger(capacity) || capacity <= 0) {
      throw new Error("capacity must be a positive safe integer");
    }
  }

  public push(value: T): void {
    if (this.entries.length >= this.capacity) throw new Error("queue full");
    this.entries.push(value);
    this.highWater = Math.max(this.highWater, this.entries.length);
  }

  public shift(): T | undefined {
    return this.entries.shift();
  }

  public get size(): number {
    return this.entries.length;
  }
}

export class WatchCursor {
  private last: bigint;
  public constructor(resumeAfter: bigint) {
    if (resumeAfter < 0n) throw new Error("sequence cannot be negative");
    this.last = resumeAfter;
  }
  public accept(sequence: bigint): "new" | "duplicate" {
    if (sequence <= this.last) return "duplicate";
    if (sequence !== this.last + 1n) throw new Error("observation gap");
    this.last = sequence;
    return "new";
  }
  public value(): bigint { return this.last; }
}

export type WorkerFrame =
  | { kind: "hello"; workerId: string; tenantId: string; maxConcurrency: number }
  | { kind: "ready"; availableSlots: number }
  | { kind: "progress"; assignmentId: string; generation: bigint; percent: number }
  | { kind: "result"; assignmentId: string; generation: bigint; success: boolean };

export class WorkerProtocol {
  private helloSeen = false;
  private workerId: string | undefined;
  public accept(frame: WorkerFrame): void {
    if (!this.helloSeen) {
      if (frame.kind !== "hello") throw new Error("first frame must be hello");
      if (frame.maxConcurrency <= 0) throw new Error("invalid concurrency");
      this.helloSeen = true;
      this.workerId = frame.workerId;
      return;
    }
    if (frame.kind === "hello") throw new Error("duplicate hello");
  }
  public identity(): string {
    if (this.workerId === undefined) throw new Error("worker not identified");
    return this.workerId;
  }
}
