import { randomUUID } from "node:crypto";
import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { setTimeout as sleep } from "node:timers/promises";

import multipart from "@fastify/multipart";
import swagger from "@fastify/swagger";
import swaggerUi from "@fastify/swagger-ui";
import Fastify, {
  type FastifyInstance,
  type FastifyReply,
  type FastifyRequest,
} from "fastify";

import { principal, requireScopes } from "./auth.js";
import { FileSystemArtifactStore } from "./artifacts.js";
import {
  settingsFromEnvironment,
  type Settings,
} from "./config.js";
import { Database } from "./db.js";
import { projectEtag } from "./domain.js";
import {
  ApiProblem,
  installProblemHandling,
} from "./problems.js";
import { PostgresRepository } from "./repository.js";
import {
  AnalysisRunCreateSchema,
  AnalysisRunPageSchema,
  AnalysisRunPageV12Schema,
  AnalysisRunSchema,
  AnalysisRunV12Schema,
  ArtifactIdParams,
  ArtifactPageSchema,
  ArtifactSchema,
  DatasetCreateSchema,
  DatasetIdParams,
  DatasetListQuery,
  DatasetPageSchema,
  DatasetSchema,
  DiagnosticsSchema,
  DiagnosticsV12Schema,
  HealthSchema,
  ProjectCreateSchema,
  ProjectIdParams,
  ProjectListQuery,
  ProjectPageSchema,
  ProjectPatchSchema,
  ProjectSchema,
  RunIdParams,
  RunListQuery,
  UploadReceiptSchema,
  WebhookSubscriptionCreateSchema,
  WebhookSubscriptionSchema,
} from "./schemas.js";
import { AnalysisService } from "./service.js";
import type {
  AnalysisRunCreate,
  DatasetCreate,
  ProjectCreate,
  ProjectPatch,
  WebhookSubscriptionCreate,
} from "./types.js";

function integer(value: unknown, fallback = 20): number {
  if (value === undefined) return fallback;
  const parsed = Number(value);
  if (!Number.isInteger(parsed)) {
    throw new ApiProblem(
      422,
      "Request validation failed",
      "Expected an integer.",
      "validation",
    );
  }
  return parsed;
}

function replyProject(
  reply: FastifyReply,
  value: Awaited<ReturnType<AnalysisService["getProject"]>>,
): unknown {
  reply.header("ETag", projectEtag(value.id, value.version));
  return value;
}

function lastEventPosition(value: string | string[] | undefined): string {
  const raw = Array.isArray(value) ? value[0] : value;
  if (raw === undefined || raw === "") return "0";
  const match = /^evt_([0-9]{4,18})$/.exec(raw);
  if (!match) {
    throw new ApiProblem(
      422,
      "Request validation failed",
      "Last-Event-ID must contain a valid event identifier.",
      "validation",
    );
  }
  return BigInt(match[1]!).toString();
}

function streamMediaType(
  value: string | string[] | undefined,
): "sse" | "ndjson" {
  const accept = Array.isArray(value) ? value.join(",") : value;
  if (!accept || accept.includes("*/*") || accept.includes("text/event-stream")) {
    return "sse";
  }
  if (accept.includes("application/x-ndjson")) return "ndjson";
  throw new ApiProblem(
    406,
    "Not acceptable",
    "Use text/event-stream or application/x-ndjson.",
    "not-acceptable",
  );
}

async function writeChunk(
  reply: FastifyReply,
  chunk: string,
): Promise<void> {
  if (reply.raw.write(chunk)) return;
  await new Promise<void>((resolve, reject) => {
    reply.raw.once("drain", resolve);
    reply.raw.once("error", reject);
  });
}

export async function buildApp(
  settings: Settings = settingsFromEnvironment(),
): Promise<FastifyInstance> {
  const app = Fastify({
    logger: {
      level: settings.environment === "test" ? "silent" : "info",
    },
    genReqId: (request) => {
      const supplied = request.headers["x-request-id"];
      return typeof supplied === "string" && /^req_[a-f0-9]{12}$/.test(supplied)
        ? supplied
        : `req_${randomUUID().replaceAll("-", "").slice(0, 12)}`;
    },
  });

  const database = new Database(settings.databaseUrl);
  const repository = new PostgresRepository(
    database,
    settings.webhookEncryptionKey,
    settings.callbackSigningSecret,
    settings.serviceRelease,
  );
  const artifacts = new FileSystemArtifactStore(settings.artifactRoot);
  const service = new AnalysisService(
    repository,
    artifacts,
    settings.uploadLimitBytes,
  );
  const runSchema = settings.serviceRelease === "1.1"
    ? AnalysisRunV12Schema
    : AnalysisRunSchema;
  const runPageSchema = settings.serviceRelease === "1.1"
    ? AnalysisRunPageV12Schema
    : AnalysisRunPageSchema;
  const diagnosticsSchema = settings.serviceRelease === "1.1"
    ? DiagnosticsV12Schema
    : DiagnosticsSchema;

  app.decorate("analysisRepository", repository);
  app.decorate("analysisService", service);
  app.addHook("onClose", async () => repository.close());
  app.addHook("onSend", async (request, reply, payload) => {
    reply.header("X-Request-Id", request.id);
    return payload;
  });

  await app.register(multipart, {
    limits: {
      fileSize: settings.uploadLimitBytes,
      files: 1,
      fields: 8,
      parts: 9,
    },
  });
  await app.register(swagger, {
    openapi: {
      info: {
        title: "Analysis Runs API — durable TypeScript provider",
        version: settings.publicApiVersion,
      },
    },
  });
  await app.register(swaggerUi, { routePrefix: "/docs" });
  installProblemHandling(app);

  app.get(
    "/health",
    {
      schema: {
        operationId: "getHealth",
        response: { 200: HealthSchema },
      },
    },
    async () => {
      await repository.health();
      return {
        status: "ok",
        service: "analysis-runs-api",
        version: settings.publicApiVersion,
        time: new Date().toISOString(),
      };
    },
  );

  app.get(
    "/projects",
    {
      preHandler: requireScopes("projects:read"),
      schema: {
        operationId: "listProjects",
        querystring: ProjectListQuery,
        response: { 200: ProjectPageSchema },
      },
    },
    async (request) => {
      const query = request.query as {
        limit?: number;
        cursor?: string;
        name?: string;
      };
      return service.listProjects(
        principal(request),
        integer(query.limit),
        query.cursor,
        query.name,
      );
    },
  );

  app.post(
    "/projects",
    {
      preHandler: requireScopes("projects:write"),
      schema: {
        operationId: "createProject",
        body: ProjectCreateSchema,
        response: { 201: ProjectSchema },
      },
    },
    async (request, reply) => {
      const value = await service.createProject(
        principal(request),
        request.body as ProjectCreate,
      );
      reply.code(201).header("Location", `/projects/${value.id}`);
      return replyProject(reply, value);
    },
  );

  app.get(
    "/projects/:projectId",
    {
      preHandler: requireScopes("projects:read"),
      schema: {
        operationId: "getProject",
        params: ProjectIdParams,
        response: { 200: ProjectSchema },
      },
    },
    async (request, reply) => {
      const { projectId } = request.params as { projectId: string };
      return replyProject(
        reply,
        await service.getProject(principal(request), projectId),
      );
    },
  );

  app.patch(
    "/projects/:projectId",
    {
      preHandler: requireScopes("projects:write"),
      schema: {
        operationId: "updateProject",
        params: ProjectIdParams,
        body: ProjectPatchSchema,
        response: { 200: ProjectSchema },
      },
    },
    async (request, reply) => {
      const { projectId } = request.params as { projectId: string };
      const raw = request.headers["if-match"];
      const ifMatch = Array.isArray(raw) ? raw[0] : raw;
      return replyProject(
        reply,
        await service.updateProject(
          principal(request),
          projectId,
          ifMatch,
          request.body as ProjectPatch,
        ),
      );
    },
  );

  app.get(
    "/projects/:projectId/datasets",
    {
      preHandler: requireScopes("datasets:read"),
      schema: {
        operationId: "listProjectDatasets",
        params: ProjectIdParams,
        querystring: DatasetListQuery,
        response: { 200: DatasetPageSchema },
      },
    },
    async (request) => {
      const { projectId } = request.params as { projectId: string };
      const query = request.query as {
        limit?: number;
        cursor?: string;
        status?: string;
      };
      return service.listDatasets(
        principal(request),
        projectId,
        integer(query.limit),
        query.cursor,
        query.status,
      );
    },
  );

  app.post(
    "/projects/:projectId/datasets",
    {
      preHandler: requireScopes("datasets:write"),
      schema: {
        operationId: "createDataset",
        params: ProjectIdParams,
        body: DatasetCreateSchema,
        response: { 201: DatasetSchema },
      },
    },
    async (request, reply) => {
      const { projectId } = request.params as { projectId: string };
      const value = await service.createDataset(
        principal(request),
        projectId,
        request.body as DatasetCreate,
      );
      return reply
        .code(201)
        .header("Location", `/datasets/${value.id}`)
        .send(value);
    },
  );

  app.get(
    "/datasets/:datasetId",
    {
      preHandler: requireScopes("datasets:read"),
      schema: {
        operationId: "getDataset",
        params: DatasetIdParams,
        response: { 200: DatasetSchema },
      },
    },
    async (request) => {
      const { datasetId } = request.params as { datasetId: string };
      return service.getDataset(principal(request), datasetId);
    },
  );

  app.delete(
    "/datasets/:datasetId",
    {
      preHandler: requireScopes("datasets:write"),
      schema: {
        operationId: "deleteDataset",
        params: DatasetIdParams,
      },
    },
    async (request, reply) => {
      const { datasetId } = request.params as { datasetId: string };
      await service.deleteDataset(principal(request), datasetId);
      return reply.code(204).send();
    },
  );

  app.post(
    "/datasets/:datasetId/content",
    {
      preHandler: requireScopes("datasets:write"),
      schema: {
        operationId: "uploadDatasetContent",
        params: DatasetIdParams,
        response: { 201: UploadReceiptSchema },
      },
    },
    async (request, reply) => {
      const { datasetId } = request.params as { datasetId: string };
      const part = await request.file();
      if (!part) {
        throw new ApiProblem(
          422,
          "Request validation failed",
          "A multipart file part is required.",
          "validation",
        );
      }
      const value = await service.uploadDataset(
        principal(request),
        datasetId,
        part,
      );
      return reply.code(201).send(value);
    },
  );

  app.get(
    "/analysis-runs",
    {
      preHandler: requireScopes("runs:read"),
      schema: {
        operationId: "listAnalysisRuns",
        querystring: RunListQuery,
        response: { 200: runPageSchema },
      },
    },
    async (request) => {
      const query = request.query as {
        limit?: number;
        cursor?: string;
        status?: string;
      };
      return service.listRuns(
        principal(request),
        integer(query.limit),
        query.cursor,
        query.status,
      );
    },
  );

  app.post(
    "/analysis-runs",
    {
      preHandler: requireScopes("runs:write"),
      schema: {
        operationId: "createAnalysisRun",
        body: AnalysisRunCreateSchema,
        response: { 202: runSchema },
      },
    },
    async (request, reply) => {
      const raw = request.headers["idempotency-key"];
      const key = Array.isArray(raw) ? raw[0] : raw;
      if (
        !key ||
        key.length < 16 ||
        key.length > 64 ||
        !/^[A-Za-z0-9._~-]+$/.test(key)
      ) {
        throw new ApiProblem(
          422,
          "Request validation failed",
          "Idempotency-Key is invalid.",
          "validation",
        );
      }
      const stored = await service.createRun(
        principal(request),
        key,
        request.body as AnalysisRunCreate,
      );
      for (const [name, value] of Object.entries(stored.headers)) {
        reply.header(name, value);
      }
      reply.header("Idempotent-Replay", stored.replay ? "true" : "false");
      return reply.code(202).send(stored.body);
    },
  );

  app.get(
    "/analysis-runs/:runId",
    {
      preHandler: requireScopes("runs:read"),
      schema: {
        operationId: "getAnalysisRun",
        params: RunIdParams,
        response: { 200: runSchema },
      },
    },
    async (request) => {
      const { runId } = request.params as { runId: string };
      return service.getRun(principal(request), runId);
    },
  );

  app.post(
    "/analysis-runs/:runId/cancellation",
    {
      preHandler: requireScopes("runs:write"),
      schema: {
        operationId: "cancelAnalysisRun",
        params: RunIdParams,
        response: { 200: runSchema },
      },
    },
    async (request) => {
      const { runId } = request.params as { runId: string };
      return service.cancelRun(principal(request), runId);
    },
  );

  app.get(
    "/analysis-runs/:runId/artifacts",
    {
      preHandler: requireScopes("artifacts:read"),
      schema: {
        operationId: "listRunArtifacts",
        params: RunIdParams,
        response: { 200: ArtifactPageSchema },
      },
    },
    async (request) => {
      const { runId } = request.params as { runId: string };
      return {
        items: await service.listArtifacts(principal(request), runId),
      };
    },
  );

  app.get(
    "/analysis-runs/:runId/events",
    {
      preHandler: requireScopes("runs:read"),
      schema: {
        operationId: "streamAnalysisRunEvents",
        params: RunIdParams,
      },
    },
    async (request, reply) => {
      const { runId } = request.params as { runId: string };
      const representation = streamMediaType(request.headers.accept);
      let after = lastEventPosition(request.headers["last-event-id"]);
      let closed = false;
      request.raw.once("close", () => {
        closed = true;
      });

      reply.hijack();
      reply.raw.writeHead(200, {
        "Content-Type": representation === "ndjson"
          ? "application/x-ndjson"
          : "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
        "X-Request-Id": request.id,
      });

      try {
        while (!closed) {
          const events = await service.events(
            principal(request),
            runId,
            after,
          );
          for (const event of events) {
            const match = /^evt_([0-9]{4,18})$/.exec(event.eventId);
            if (!match) throw new Error("database returned an invalid event id");
            after = BigInt(match[1]!).toString();
            const json = JSON.stringify(event);
            await writeChunk(
              reply,
              representation === "ndjson"
                ? `${json}\n`
                : `id: ${event.eventId}\nevent: progress\ndata: ${json}\n\n`,
            );
            if (["completed", "failed", "canceled"].includes(event.status)) {
              reply.raw.end();
              return;
            }
          }
          await sleep(250);
        }
      } catch (error) {
        if (!closed) reply.raw.destroy(error as Error);
      }
    },
  );

  app.get(
    "/artifacts/:artifactId",
    {
      preHandler: requireScopes("artifacts:read"),
      schema: {
        operationId: "getArtifact",
        params: ArtifactIdParams,
        response: { 200: ArtifactSchema },
      },
    },
    async (request) => {
      const { artifactId } = request.params as { artifactId: string };
      return service.getArtifact(principal(request), artifactId);
    },
  );

  if (settings.serviceRelease === "1.1") {
    app.get(
      "/artifacts/:artifactId/content",
      {
        preHandler: requireScopes("artifacts:read"),
        schema: {
          operationId: "downloadArtifactContent",
          params: ArtifactIdParams,
        },
      },
      async (request, reply) => {
        const { artifactId } = request.params as { artifactId: string };
        const { artifact, path } = await service.artifactFile(
          principal(request),
          artifactId,
        );
        const etag = `"sha256:${artifact.checksumSha256}"`;
        if (request.headers["if-none-match"] === etag) {
          return reply.code(304).header("ETag", etag).send();
        }
        const metadata = await stat(path);
        reply
          .header("Content-Type", artifact.mediaType)
          .header("Content-Length", String(metadata.size))
          .header("ETag", etag)
          .header(
            "Content-Disposition",
            `attachment; filename="${artifact.name.replaceAll('"', '')}"`,
          );
        return reply.send(createReadStream(path));
      },
    );
  }

  app.post(
    "/webhook-subscriptions",
    {
      preHandler: requireScopes("webhooks:write"),
      schema: {
        operationId: "createWebhookSubscription",
        body: WebhookSubscriptionCreateSchema,
        response: { 201: WebhookSubscriptionSchema },
      },
    },
    async (request, reply) => {
      const body = request.body as WebhookSubscriptionCreate;
      const value = await service.createSubscription(
        principal(request),
        body,
      );
      return reply
        .code(201)
        .header("Location", `/webhook-subscriptions/${value.id}`)
        .send(value);
    },
  );

  app.get(
    "/internal/diagnostics",
    {
      preHandler: requireScopes("admin"),
      schema: {
        operationId: "getInternalDiagnostics",
        response: { 200: diagnosticsSchema },
      },
    },
    async () => repository.diagnostics(),
  );

  return app;
}
