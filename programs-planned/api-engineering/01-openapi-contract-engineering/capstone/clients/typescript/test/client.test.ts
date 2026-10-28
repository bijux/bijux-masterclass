import { describe, expect, it } from "vitest";

import { AnalysisClient, ApiError } from "../src/client.js";

const json = (status: number, body: unknown, headers: Record<string, string> = {}): Response =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...headers },
  });

const project = {
  id: "prj_0001",
  ownerId: "learner",
  name: "Demo",
  description: null,
  version: 1,
  createdAt: "2026-08-05T10:00:00Z",
  updatedAt: "2026-08-05T10:00:00Z",
};
const dataset = {
  id: "dts_0001",
  projectId: "prj_0001",
  ownerId: "learner",
  name: "dataset",
  source: { kind: "local-file", fileName: "dataset.csv", mediaType: "text/csv" },
  status: "awaiting-upload",
  contentLength: null,
  checksumSha256: null,
  createdAt: "2026-08-05T10:00:00Z",
  updatedAt: "2026-08-05T10:00:00Z",
} as const;

const run = (status: "queued" | "running" | "completed") => ({
  id: "run_0001",
  projectId: "prj_0001",
  datasetId: "dts_0001",
  ownerId: "learner",
  status,
  parameters: { algorithm: "quality-summary", priority: "normal", labels: {} },
  progress: status === "queued" ? 0 : status === "running" ? 50 : 100,
  createdAt: "2026-08-05T10:02:00Z",
  updatedAt: "2026-08-05T10:03:00Z",
  completedAt: status === "completed" ? "2026-08-05T10:03:00Z" : null,
  artifactIds: status === "completed" ? ["art_0001"] : [],
});

describe("AnalysisClient", () => {
  it("executes the workflow and preserves contract headers", async () => {
    let poll = 0;
    const observed: Array<[string, string]> = [];
    const fetcher: typeof fetch = async (input, init = {}) => {
      const url = new URL(String(input));
      const method = init.method ?? "GET";
      observed.push([method, url.pathname]);
      const headers = new Headers(init.headers);
      expect(headers.get("authorization")).toBe("Bearer learner-write");

      if (method === "POST" && url.pathname === "/projects") {
        return json(201, project, { ETag: '"prj_0001:1"', Location: "/projects/prj_0001" });
      }
      if (method === "POST" && url.pathname === "/projects/prj_0001/datasets") {
        return json(201, dataset);
      }
      if (method === "POST" && url.pathname === "/datasets/dts_0001/content") {
        expect(init.body).toBeInstanceOf(FormData);
        return json(201, {
          datasetId: "dts_0001",
          contentLength: 17,
          checksumSha256: "a".repeat(64),
          uploadedAt: "2026-08-05T10:01:00Z",
        });
      }
      if (method === "POST" && url.pathname === "/analysis-runs") {
        expect(headers.get("idempotency-key")).toBe("typescript-client-test-0001");
        return json(202, run("queued"), {
          Location: "/analysis-runs/run_0001",
          "Idempotent-Replay": "false",
        });
      }
      if (method === "GET" && url.pathname === "/analysis-runs/run_0001") {
        poll += 1;
        return json(200, run(poll === 1 ? "running" : "completed"));
      }
      if (method === "GET" && url.pathname === "/analysis-runs/run_0001/artifacts") {
        return json(200, {
          items: [
            {
              id: "art_0001",
              runId: "run_0001",
              ownerId: "learner",
              name: "quality-summary.json",
              mediaType: "application/json",
              size: 80,
              checksumSha256: "b".repeat(64),
              createdAt: "2026-08-05T10:03:00Z",
            },
          ],
        });
      }
      throw new Error(`unexpected request: ${method} ${url.pathname}`);
    };

    const client = new AnalysisClient("https://api.example.test", {
      bearerToken: "learner-write",
      fetch: fetcher,
    });
    const created = await client.createProject("Demo");
    const registered = await client.registerLocalDataset(created.id, "dataset", "dataset.csv");
    await client.uploadDatasetContent(registered.id, new Blob(["sample,value\nA,1\n"]), "dataset.csv");
    const accepted = await client.startRun(created.id, registered.id, "typescript-client-test-0001");
    const completed = await client.waitForRun(accepted.id);
    const artifacts = await client.listArtifacts(completed.id);

    expect(created._etag).toBe('"prj_0001:1"');
    expect(completed.status).toBe("completed");
    expect(artifacts[0]?.id).toBe("art_0001");
    expect(observed.at(-1)).toEqual(["GET", "/analysis-runs/run_0001/artifacts"]);
  });

  it("turns Problem Details into a typed exception", async () => {
    const fetcher: typeof fetch = async () =>
      new Response(
        JSON.stringify({
          type: "https://api.example.test/problems/conflict",
          title: "Request conflict",
          status: 409,
          detail: "The run is already complete.",
          requestId: "req_012345abcdef",
        }),
        { status: 409, headers: { "Content-Type": "application/problem+json" } },
      );
    const client = new AnalysisClient("https://api.example.test", {
      bearerToken: "learner-write",
      fetch: fetcher,
    });
    await expect(client.listArtifacts("run_0001")).rejects.toMatchObject<ApiError>({
      status: 409,
      requestId: "req_012345abcdef",
    });
  });

  it("requires exactly one authentication mode", () => {
    expect(() => new AnalysisClient("https://api.example.test", {})).toThrow(TypeError);
    expect(
      () =>
        new AnalysisClient("https://api.example.test", {
          bearerToken: "learner-write",
          apiKey: "demo-api-key",
        }),
    ).toThrow(TypeError);
  });
});
