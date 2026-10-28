import { createHash } from "node:crypto";

export function partitionFor(key: string, partitionCount: number): number {
  if (!key) throw new Error("partition key cannot be blank");
  if (!Number.isSafeInteger(partitionCount) || partitionCount <= 0) {
    throw new Error("partition count must be a positive safe integer");
  }
  const digest = createHash("sha256").update(key).digest();
  let value = 0n;
  for (let index = 0; index < 8; index += 1) {
    value = (value << 8n) + BigInt(digest[index] ?? 0);
  }
  return Number(value % BigInt(partitionCount));
}
