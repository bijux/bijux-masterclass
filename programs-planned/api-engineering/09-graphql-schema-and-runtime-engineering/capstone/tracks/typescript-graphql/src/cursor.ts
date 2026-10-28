import { createHash, createHmac, timingSafeEqual } from "node:crypto";

import { ValidationError, type Principal } from "./model.js";

export interface CursorState {
  tenantId: string;
  audienceHash: string;
  scope: string;
  filterHash: string;
  afterPrimary: string;
  afterTiebreaker: string;
  highWaterPrimary: string;
  highWaterTiebreaker: string;
  expiresAt: number;
  version: number;
}

export function stableJson(value: unknown): string {
  if (Array.isArray(value)) {
    return `[${value.map(stableJson).join(",")}]`;
  }
  if (value !== null && typeof value === "object") {
    const entries = Object.entries(value as Record<string, unknown>)
      .sort(([left], [right]) => left.localeCompare(right))
      .map(([key, item]) => `${JSON.stringify(key)}:${stableJson(item)}`);
    return `{${entries.join(",")}}`;
  }
  return JSON.stringify(value);
}

export function normalizedFilterHash(value: Record<string, unknown>): string {
  return createHash("sha256").update(stableJson(value)).digest("hex");
}

export function audienceHash(principal: Principal): string {
  return createHash("sha256")
    .update(
      stableJson({
        permissions: [...principal.permissions].sort(),
        subject: principal.subject,
        tenant: principal.tenantId,
      }),
    )
    .digest("hex");
}

function compareKey(
  left: readonly [string, string],
  right: readonly [string, string],
): number {
  return left[0].localeCompare(right[0]) || left[1].localeCompare(right[1]);
}

export class CursorCodec {
  constructor(private readonly key: Uint8Array) {
    if (key.length < 32) {
      throw new Error("cursor key must be at least 32 bytes");
    }
  }

  encode(state: CursorState): string {
    if (!state.scope || !state.tenantId) {
      throw new ValidationError("cursor scope and tenant are required");
    }
    if (!Number.isSafeInteger(state.expiresAt) || state.expiresAt <= 0) {
      throw new ValidationError("cursor expiry is invalid");
    }
    if (
      compareKey(
        [state.afterPrimary, state.afterTiebreaker],
        [state.highWaterPrimary, state.highWaterTiebreaker],
      ) > 0
    ) {
      throw new ValidationError("cursor continuation exceeds high-water key");
    }

    const payload = Buffer.from(
      stableJson({
        a: state.audienceHash,
        e: state.expiresAt,
        f: state.filterHash,
        ha: state.highWaterPrimary,
        hb: state.highWaterTiebreaker,
        pa: state.afterPrimary,
        pb: state.afterTiebreaker,
        s: state.scope,
        t: state.tenantId,
        v: state.version,
      }),
      "utf8",
    );
    const signature = createHmac("sha256", this.key).update(payload).digest();
    return Buffer.concat([payload, signature]).toString("base64url");
  }

  decode(
    value: string,
    expected: {
      tenantId: string;
      audienceHash: string;
      scope: string;
      filterHash: string;
      nowEpoch: number;
    },
  ): CursorState {
    try {
      const raw = Buffer.from(value, "base64url");
      if (raw.length <= 32) {
        throw new ValidationError("malformed cursor");
      }
      const payload = raw.subarray(0, raw.length - 32);
      const signature = raw.subarray(raw.length - 32);
      const calculated = createHmac("sha256", this.key).update(payload).digest();
      if (
        signature.length !== calculated.length ||
        !timingSafeEqual(signature, calculated)
      ) {
        throw new ValidationError("invalid cursor signature");
      }

      const rawState = JSON.parse(payload.toString("utf8")) as Record<
        string,
        unknown
      >;
      const state: CursorState = {
        tenantId: String(rawState.t),
        audienceHash: String(rawState.a),
        scope: String(rawState.s),
        filterHash: String(rawState.f),
        afterPrimary: String(rawState.pa),
        afterTiebreaker: String(rawState.pb),
        highWaterPrimary: String(rawState.ha),
        highWaterTiebreaker: String(rawState.hb),
        expiresAt: Number(rawState.e),
        version: Number(rawState.v),
      };

      if (state.version !== 1) {
        throw new ValidationError("unsupported cursor version");
      }
      if (state.tenantId !== expected.tenantId) {
        throw new ValidationError("cursor tenant mismatch");
      }
      if (state.audienceHash !== expected.audienceHash) {
        throw new ValidationError("cursor audience mismatch");
      }
      if (state.scope !== expected.scope) {
        throw new ValidationError("cursor scope mismatch");
      }
      if (state.filterHash !== expected.filterHash) {
        throw new ValidationError("cursor filter mismatch");
      }
      if (!Number.isSafeInteger(state.expiresAt) || state.expiresAt < expected.nowEpoch) {
        throw new ValidationError("cursor expired");
      }
      if (
        compareKey(
          [state.afterPrimary, state.afterTiebreaker],
          [state.highWaterPrimary, state.highWaterTiebreaker],
        ) > 0
      ) {
        throw new ValidationError("invalid cursor key order");
      }
      return state;
    } catch (error) {
      if (error instanceof ValidationError) {
        throw error;
      }
      throw new ValidationError("malformed cursor");
    }
  }
}
