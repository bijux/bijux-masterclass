import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

import { describe, expect, it } from "vitest";

const baseline = [
  "getHealth",
  "listProjects",
  "createProject",
  "getProject",
  "updateProject",
  "listProjectDatasets",
  "createDataset",
  "getDataset",
  "deleteDataset",
  "uploadDatasetContent",
  "listAnalysisRuns",
  "createAnalysisRun",
  "getAnalysisRun",
  "cancelAnalysisRun",
  "listRunArtifacts",
  "streamAnalysisRunEvents",
  "getArtifact",
  "createWebhookSubscription",
  "getInternalDiagnostics",
];

describe("operation ownership", () => {
  it("maps every frozen operation exactly once", async () => {
    const source = await readFile(resolve("src/app.ts"), "utf8");
    for (const operation of baseline) {
      expect(
        source.match(new RegExp(`operationId:\\s*\"${operation}\"`, "g"))
          ?.length,
      ).toBe(1);
    }
  });

  it("owns the additive API 1.2 operation exactly once", async () => {
    const source = await readFile(resolve("src/app.ts"), "utf8");
    expect(
      source.match(/operationId:\s*"downloadArtifactContent"/g)?.length,
    ).toBe(1);
  });
});
