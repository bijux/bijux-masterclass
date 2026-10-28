import { describe, expect, it } from "vitest";

import {
  canonicalJson,
  filterFingerprint,
  parseCursor,
  parseProjectEtag,
  projectEtag,
  requestFingerprint,
  retryDelaySeconds,
  verifyWebhookSignature,
  webhookSignature,
} from "../src/domain.js";

const WEBHOOK_BODY = Buffer.from(
  '{"eventId":"evt_0001","eventType":"analysis.completed","runId":"run_0001"}',
  "utf8",
);

describe("durable boundary primitives", () => {
  it("binds entity tags to resource and version", () => {
    const etag = projectEtag("prj_0001", 7);
    expect(parseProjectEtag(etag, "prj_0001")).toBe(7);
    expect(() => parseProjectEtag(etag, "prj_0002")).toThrow();
  });

  it("keeps PostgreSQL bigint cursor handles as strings", () => {
    expect(parseCursor(undefined)).toBeUndefined();
    expect(parseCursor("17")).toBe("17");
    expect(parseCursor("9223372036854775807")).toBe(
      "9223372036854775807",
    );
    expect(() => parseCursor("9223372036854775808")).toThrow();
    expect(() => parseCursor("17:anything")).toThrow();
  });

  it("canonicalizes request fingerprints", () => {
    expect(
      requestFingerprint("createAnalysisRun", "learner", { b: 2, a: 1 }),
    ).toBe(
      requestFingerprint("createAnalysisRun", "learner", { a: 1, b: 2 }),
    );
    expect(
      requestFingerprint("createAnalysisRun", "learner", { a: 1 }),
    ).not.toBe(
      requestFingerprint("createAnalysisRun", "learner", { a: 2 }),
    );
  });

  it("binds cursors to operation, principal, and filters", () => {
    expect(filterFingerprint("listProjects", "learner", { name: null }))
      .not.toBe(filterFingerprint("listRuns", "learner", { name: null }));
    expect(filterFingerprint("listProjects", "learner", { name: null }))
      .not.toBe(filterFingerprint("listProjects", "other", { name: null }));
  });

  it("uses the documented deterministic JSON profile", () => {
    expect(canonicalJson({ b: 2, a: [2, 1] })).toBe(
      '{"a":[2,1],"b":2}',
    );
    expect(() => canonicalJson([undefined])).toThrow();
  });

  it("matches the cross-language webhook vector", () => {
    const signature = webhookSignature(
      "course-callback-signing-secret",
      "1700000000",
      WEBHOOK_BODY,
    );
    expect(signature).toBe(
      "sha256=7fe00dbc1737f3cffaf66adcad12576f40959bb9dd4f797587342dfe69f48f13",
    );
    expect(
      verifyWebhookSignature(
        "course-callback-signing-secret",
        "1700000000",
        WEBHOOK_BODY,
        signature,
      ),
    ).toBe(true);
  });

  it("bounds retry delay", () => {
    expect(retryDelaySeconds(1)).toBe(1);
    expect(retryDelaySeconds(100)).toBe(300);
  });
});
