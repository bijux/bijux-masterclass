import type { FastifyInstance } from "fastify";
import { afterEach, beforeEach, expect, it } from "vitest";

import { buildApp } from "../src/app.js";

let app: FastifyInstance;

beforeEach(async () => {
  app = await buildApp();
  await app.ready();
});

afterEach(async () => {
  await app.close();
});

it("publishes the exact canonical path-operation identifiers", () => {
  const generated = app.swagger() as {
    paths: Record<string, Record<string, { operationId?: string }>>;
  };
  const observed = new Set<string>();
  for (const pathItem of Object.values(generated.paths)) {
    for (const operation of Object.values(pathItem)) {
      if (operation.operationId) {
        observed.add(operation.operationId);
      }
    }
  }
  expect(observed).toEqual(
    new Set([
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
    ]),
  );
});
