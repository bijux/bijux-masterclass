import type { FastifyInstance } from "fastify";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import { buildApp } from "../src/app.js";
import { store } from "../src/store.js";
import { createReadyDataset, writeHeaders } from "./helpers.js";

let app: FastifyInstance;

beforeEach(async () => {
  store.reset();
  app = await buildApp();
  await app.ready();
});

afterEach(async () => {
  await app.close();
});

describe("analysis workflow", () => {
  it("completes one workflow and replays the idempotent submission", async () => {
    const { projectId, datasetId } = await createReadyDataset(app);
    const payload = {
      projectId,
      datasetId,
      parameters: { algorithm: "quality-summary", priority: "normal" },
    };
    const headers = {
      ...writeHeaders,
      "idempotency-key": "analysis-workflow-0001",
    };

    const accepted = await app.inject({
      method: "POST",
      url: "/analysis-runs",
      headers,
      payload,
    });
    expect(accepted.statusCode).toBe(202);
    expect(accepted.headers["idempotent-replay"]).toBe("false");
    const runId = accepted.json<{ id: string }>().id;

    const replay = await app.inject({
      method: "POST",
      url: "/analysis-runs",
      headers,
      payload,
    });
    expect(replay.statusCode).toBe(202);
    expect(replay.json<{ id: string }>().id).toBe(runId);
    expect(replay.headers["idempotent-replay"]).toBe("true");

    const changed = await app.inject({
      method: "POST",
      url: "/analysis-runs",
      headers,
      payload: {
        ...payload,
        parameters: { algorithm: "checksum" },
      },
    });
    expect(changed.statusCode).toBe(409);

    const first = await app.inject({
      method: "GET",
      url: `/analysis-runs/${runId}`,
      headers: writeHeaders,
    });
    const second = await app.inject({
      method: "GET",
      url: `/analysis-runs/${runId}`,
      headers: writeHeaders,
    });
    expect(second.json<{ status: string }>().status).toBe(
      first.json<{ status: string }>().status,
    );

    let completed = second;
    for (let attempt = 0; attempt < 200; attempt += 1) {
      completed = await app.inject({
        method: "GET",
        url: `/analysis-runs/${runId}`,
        headers: writeHeaders,
      });
      if (completed.json<{ status: string }>().status === "completed") break;
      await new Promise((resolve) => setTimeout(resolve, 10));
    }
    expect(completed.json<{ status: string }>().status).toBe("completed");

    const artifacts = await app.inject({
      method: "GET",
      url: `/analysis-runs/${runId}/artifacts`,
      headers: writeHeaders,
    });
    expect(artifacts.statusCode).toBe(200);
    expect(artifacts.json<{ items: unknown[] }>().items).toHaveLength(1);
  });

  it("supports a finite NDJSON progress stream", async () => {
    const { projectId, datasetId } = await createReadyDataset(app);
    const accepted = await app.inject({
      method: "POST",
      url: "/analysis-runs",
      headers: {
        ...writeHeaders,
        "idempotency-key": "analysis-workflow-0002",
      },
      payload: {
        projectId,
        datasetId,
        parameters: { algorithm: "line-count" },
      },
    });
    const runId = accepted.json<{ id: string }>().id;

    const stream = await app.inject({
      method: "GET",
      url: `/analysis-runs/${runId}/events`,
      headers: {
        ...writeHeaders,
        accept: "application/x-ndjson",
      },
    });
    expect(stream.statusCode).toBe(200);
    const lines = stream.body.split("\n").filter(Boolean);
    expect(lines.length).toBeGreaterThanOrEqual(2);
    expect(JSON.parse(lines.at(-1) as string)).toMatchObject({ status: "completed" });
  });

  it("requires admin for internal diagnostics", async () => {
    const denied = await app.inject({
      method: "GET",
      url: "/internal/diagnostics",
      headers: writeHeaders,
    });
    expect(denied.statusCode).toBe(403);

    const allowed = await app.inject({
      method: "GET",
      url: "/internal/diagnostics",
      headers: { authorization: "Bearer admin" },
    });
    expect(allowed.statusCode).toBe(200);
  });

  it("does not return webhook secrets", async () => {
    const response = await app.inject({
      method: "POST",
      url: "/webhook-subscriptions",
      headers: writeHeaders,
      payload: {
        targetUrl: "https://hooks.example.test/team-a",
        eventTypes: ["analysis.completed"],
        secret: "training-secret-0001",
      },
    });
    expect(response.statusCode).toBe(201);
    expect(response.json()).not.toHaveProperty("secret");
    expect(response.json()).toMatchObject({ secretHint: "****0001" });
  });
});
