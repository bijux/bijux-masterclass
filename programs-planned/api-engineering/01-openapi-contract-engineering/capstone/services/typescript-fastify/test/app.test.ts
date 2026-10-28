import type { FastifyInstance } from "fastify";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import { buildApp } from "../src/app.js";
import { store } from "../src/store.js";
import { writeHeaders } from "./helpers.js";

let app: FastifyInstance;

beforeEach(async () => {
  store.reset();
  app = await buildApp();
  await app.ready();
});

afterEach(async () => {
  await app.close();
});

describe("projects and public errors", () => {
  it("keeps health anonymous", async () => {
    const response = await app.inject({ method: "GET", url: "/health" });
    expect(response.statusCode).toBe(200);
    expect(response.json()).toMatchObject({ status: "ok", service: "analysis-runs-api" });
    expect(response.headers["x-request-id"]).toMatch(/^req_[a-f0-9]{12}$/);
  });

  it("uses Problem Details for missing credentials", async () => {
    const response = await app.inject({ method: "GET", url: "/projects" });
    expect(response.statusCode).toBe(401);
    expect(response.headers["content-type"]).toContain("application/problem+json");
    expect(response.json()).toMatchObject({
      status: 401,
      type: "https://api.example.test/problems/unauthorized",
    });
  });

  it("creates and conditionally updates a project", async () => {
    const created = await app.inject({
      method: "POST",
      url: "/projects",
      headers: writeHeaders,
      payload: { name: "Summer cohort", description: "Initial" },
    });
    expect(created.statusCode).toBe(201);
    const projectId = created.json<{ id: string }>().id;
    const etag = created.headers.etag;
    expect(etag).toBe('"prj_0001:1"');

    const stale = await app.inject({
      method: "PATCH",
      url: `/projects/${projectId}`,
      headers: { ...writeHeaders, "if-match": '"prj_0001:99"' },
      payload: { description: "wrong" },
    });
    expect(stale.statusCode).toBe(412);

    const updated = await app.inject({
      method: "PATCH",
      url: `/projects/${projectId}`,
      headers: { ...writeHeaders, "if-match": etag as string },
      payload: { description: null },
    });
    expect(updated.statusCode).toBe(200);
    expect(updated.json()).toMatchObject({ version: 2, description: null });
  });

  it("does not silently discard undeclared input", async () => {
    const response = await app.inject({
      method: "POST",
      url: "/projects",
      headers: writeHeaders,
      payload: { name: "Project", ownerId: "attacker" },
    });
    expect(response.statusCode).toBe(422);
    expect(response.json<{ errors: unknown[] }>().errors.length).toBeGreaterThan(0);
  });

  it("enforces scope and ownership independently", async () => {
    const created = await app.inject({
      method: "POST",
      url: "/projects",
      headers: writeHeaders,
      payload: { name: "Owned" },
    });
    const projectId = created.json<{ id: string }>().id;

    const readOnlyWrite = await app.inject({
      method: "POST",
      url: "/projects",
      headers: { authorization: "Bearer learner-read" },
      payload: { name: "Denied" },
    });
    expect(readOnlyWrite.statusCode).toBe(403);

    const otherOwner = await app.inject({
      method: "GET",
      url: `/projects/${projectId}`,
      headers: { authorization: "Bearer other-owner" },
    });
    expect(otherOwner.statusCode).toBe(404);
  });
});
