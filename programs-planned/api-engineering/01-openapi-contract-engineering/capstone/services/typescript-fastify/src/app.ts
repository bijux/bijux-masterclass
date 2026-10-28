import { randomBytes } from "node:crypto";
import { Readable } from "node:stream";

import multipart from "@fastify/multipart";
import swagger from "@fastify/swagger";
import swaggerUi from "@fastify/swagger-ui";
import { Type } from "@sinclair/typebox";
import Fastify, {
  type FastifyInstance,
  type FastifySchema,
} from "fastify";

import { principal, requireScopes } from "./auth.js";
import { ApiProblem, installProblemHandling } from "./problems.js";
import {
  AnalysisRunCreateSchema,
  AnalysisRunPageSchema,
  AnalysisRunSchema,
  ArtifactIdParams,
  ArtifactPageSchema,
  ArtifactSchema,
  DatasetCreateSchema,
  DatasetIdParams,
  DatasetPageSchema,
  DatasetSchema,
  DiagnosticsSchema,
  HealthSchema,
  ProblemSchema,
  ProjectCreateSchema,
  ProjectIdParams,
  ProjectPageSchema,
  ProjectPatchSchema,
  ProjectSchema,
  RunIdParams,
  UploadReceiptSchema,
  ValidationProblemSchema,
  WebhookSubscriptionCreateSchema,
  WebhookSubscriptionSchema,
} from "./schemas.js";
import { store } from "./store.js";
import type {
  AnalysisRun,
  AnalysisRunCreate,
  DatasetCreate,
  ProjectCreate,
  ProjectPatch,
  WebhookSubscriptionCreate,
} from "./types.js";

const schema = (value: Record<string, unknown>): FastifySchema => value as FastifySchema;

const protectedErrors = {
  401: ProblemSchema,
  403: ProblemSchema,
  422: ValidationProblemSchema,
};

const pageFields = {
  limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 50, default: 20 })),
  cursor: Type.Optional(Type.String({ pattern: "^[0-9]+$" })),
};

export async function buildApp(): Promise<FastifyInstance> {
  const app = Fastify({
    logger: false,
    genReqId: () => `req_${randomBytes(6).toString("hex")}`,
    ajv: {
      customOptions: {
        allErrors: true,
        coerceTypes: true,
        removeAdditional: false,
      },
    },
  });

  await app.register(multipart, {
    limits: {
      files: 1,
      fileSize: 1_048_577,
      fields: 1,
    },
  });

  await app.register(swagger, {
    openapi: {
      info: {
        title: "Analysis Runs API — TypeScript provider",
        version: "1.0.0",
      },
    },
  });
  await app.register(swaggerUi, { routePrefix: "/docs" });

  installProblemHandling(app);

  app.addHook("onSend", async (request, reply, payload) => {
    reply.header("X-Request-Id", request.id);
    return payload;
  });

  const simulator = setInterval(() => store.advanceSimulation(), 10);
  simulator.unref();
  app.addHook("onClose", async () => clearInterval(simulator));

  app.get(
    "/health",
    {
      schema: schema({
        operationId: "getHealth",
        tags: ["System"],
        summary: "Check service health",
        response: { 200: HealthSchema },
      }),
    },
    async () => ({
      status: "ok",
      service: "analysis-runs-api",
      version: "1.0.0",
      time: new Date().toISOString(),
    }),
  );

  app.get(
    "/projects",
    {
      preHandler: requireScopes("projects:read"),
      schema: schema({
        operationId: "listProjects",
        tags: ["Projects"],
        summary: "List projects",
        querystring: Type.Object(
          {
            ...pageFields,
            name: Type.Optional(Type.String({ minLength: 1, maxLength: 80 })),
          },
          { additionalProperties: false },
        ),
        response: { 200: ProjectPageSchema, ...protectedErrors },
      }),
    },
    async (request) => {
      const query = request.query as { limit?: number; cursor?: string; name?: string };
      return store.listProjects(principal(request), query.limit ?? 20, query.cursor, query.name);
    },
  );

  app.post(
    "/projects",
    {
      preHandler: requireScopes("projects:write"),
      schema: schema({
        operationId: "createProject",
        tags: ["Projects"],
        summary: "Create a project",
        body: ProjectCreateSchema,
        response: { 201: ProjectSchema, ...protectedErrors },
      }),
    },
    async (request, reply) => {
      const project = store.createProject(principal(request), request.body as ProjectCreate);
      return reply
        .code(201)
        .header("Location", `/projects/${project.id}`)
        .header("ETag", store.etag(project))
        .send(project);
    },
  );

  app.get(
    "/projects/:projectId",
    {
      preHandler: requireScopes("projects:read"),
      schema: schema({
        operationId: "getProject",
        tags: ["Projects"],
        summary: "Retrieve a project",
        params: ProjectIdParams,
        response: { 200: ProjectSchema, 404: ProblemSchema, ...protectedErrors },
      }),
    },
    async (request, reply) => {
      const { projectId } = request.params as { projectId: string };
      const project = store.getProject(projectId, principal(request));
      return reply.header("ETag", store.etag(project)).send(project);
    },
  );

  app.patch(
    "/projects/:projectId",
    {
      preHandler: requireScopes("projects:write"),
      schema: schema({
        operationId: "updateProject",
        tags: ["Projects"],
        summary: "Conditionally update a project",
        params: ProjectIdParams,
        headers: Type.Object(
          {
            "if-match": Type.Optional(
              Type.String({ pattern: '^"prj_[0-9]{4,18}:[0-9]+"$' }),
            ),
          },
          { additionalProperties: true },
        ),
        body: ProjectPatchSchema,
        response: {
          200: ProjectSchema,
          404: ProblemSchema,
          412: ProblemSchema,
          428: ProblemSchema,
          ...protectedErrors,
        },
      }),
    },
    async (request, reply) => {
      const { projectId } = request.params as { projectId: string };
      const ifMatchHeader = request.headers["if-match"];
      const ifMatch = Array.isArray(ifMatchHeader) ? ifMatchHeader[0] : ifMatchHeader;
      const project = store.updateProject(
        projectId,
        principal(request),
        ifMatch,
        request.body as ProjectPatch,
      );
      return reply.header("ETag", store.etag(project)).send(project);
    },
  );

  app.get(
    "/projects/:projectId/datasets",
    {
      preHandler: requireScopes("datasets:read"),
      schema: schema({
        operationId: "listProjectDatasets",
        tags: ["Datasets"],
        summary: "List project datasets",
        params: ProjectIdParams,
        querystring: Type.Object(
          {
            ...pageFields,
            status: Type.Optional(
              Type.Union([Type.Literal("awaiting-upload"), Type.Literal("ready")]),
            ),
          },
          { additionalProperties: false },
        ),
        response: { 200: DatasetPageSchema, 404: ProblemSchema, ...protectedErrors },
      }),
    },
    async (request) => {
      const { projectId } = request.params as { projectId: string };
      const query = request.query as {
        limit?: number;
        cursor?: string;
        status?: "awaiting-upload" | "ready";
      };
      return store.listDatasets(
        projectId,
        principal(request),
        query.limit ?? 20,
        query.cursor,
        query.status,
      );
    },
  );

  app.post(
    "/projects/:projectId/datasets",
    {
      preHandler: requireScopes("datasets:write"),
      schema: schema({
        operationId: "createDataset",
        tags: ["Datasets"],
        summary: "Register a dataset",
        params: ProjectIdParams,
        body: DatasetCreateSchema,
        response: { 201: DatasetSchema, 404: ProblemSchema, ...protectedErrors },
      }),
    },
    async (request, reply) => {
      const { projectId } = request.params as { projectId: string };
      const dataset = store.createDataset(
        projectId,
        principal(request),
        request.body as DatasetCreate,
      );
      return reply
        .code(201)
        .header("Location", `/datasets/${dataset.id}`)
        .send(dataset);
    },
  );

  app.get(
    "/datasets/:datasetId",
    {
      preHandler: requireScopes("datasets:read"),
      schema: schema({
        operationId: "getDataset",
        tags: ["Datasets"],
        summary: "Retrieve a dataset",
        params: DatasetIdParams,
        response: { 200: DatasetSchema, 404: ProblemSchema, ...protectedErrors },
      }),
    },
    async (request) => {
      const { datasetId } = request.params as { datasetId: string };
      return store.getDataset(datasetId, principal(request));
    },
  );

  app.delete(
    "/datasets/:datasetId",
    {
      preHandler: requireScopes("datasets:write"),
      schema: schema({
        operationId: "deleteDataset",
        tags: ["Datasets"],
        summary: "Delete a dataset",
        params: DatasetIdParams,
        response: {
          204: Type.Null(),
          404: ProblemSchema,
          409: ProblemSchema,
          ...protectedErrors,
        },
      }),
    },
    async (request, reply) => {
      const { datasetId } = request.params as { datasetId: string };
      store.deleteDataset(datasetId, principal(request));
      return reply.code(204).send();
    },
  );

  app.post(
    "/datasets/:datasetId/content",
    {
      preHandler: requireScopes("datasets:write"),
      schema: schema({
        operationId: "uploadDatasetContent",
        tags: ["Datasets"],
        summary: "Upload local dataset content",
        params: DatasetIdParams,
        response: {
          201: UploadReceiptSchema,
          404: ProblemSchema,
          409: ProblemSchema,
          413: ProblemSchema,
          415: ProblemSchema,
          ...protectedErrors,
        },
      }),
    },
    async (request, reply) => {
      const { datasetId } = request.params as { datasetId: string };
      const part = await request.file();
      if (!part) {
        throw new ApiProblem(422, "Request validation failed", "A file part is required.", "validation");
      }
      let content: Buffer;
      try {
        content = await part.toBuffer();
      } catch (error) {
        if (error instanceof Error && error.message.toLowerCase().includes("file too large")) {
          throw new ApiProblem(
            413,
            "Payload too large",
            "The training upload limit is 1 MiB.",
            "payload-too-large",
          );
        }
        throw error;
      }
      const receipt = store.uploadDataset(
        datasetId,
        principal(request),
        content,
        part.mimetype,
      );
      return reply.code(201).send(receipt);
    },
  );

  app.get(
    "/analysis-runs",
    {
      preHandler: requireScopes("runs:read"),
      schema: schema({
        operationId: "listAnalysisRuns",
        tags: ["Analysis Runs"],
        summary: "List analysis runs",
        querystring: Type.Object(
          {
            ...pageFields,
            status: Type.Optional(
              Type.Union([
                Type.Literal("queued"),
                Type.Literal("running"),
                Type.Literal("completed"),
                Type.Literal("failed"),
                Type.Literal("canceled"),
              ]),
            ),
          },
          { additionalProperties: false },
        ),
        response: { 200: AnalysisRunPageSchema, ...protectedErrors },
      }),
    },
    async (request) => {
      const query = request.query as {
        limit?: number;
        cursor?: string;
        status?: AnalysisRun["status"];
      };
      return store.listRuns(
        principal(request),
        query.limit ?? 20,
        query.cursor,
        query.status,
      );
    },
  );

  app.post(
    "/analysis-runs",
    {
      preHandler: requireScopes("runs:write"),
      schema: schema({
        operationId: "createAnalysisRun",
        tags: ["Analysis Runs"],
        summary: "Start an analysis run",
        headers: Type.Object(
          {
            "idempotency-key": Type.String({
              minLength: 16,
              maxLength: 64,
              pattern: "^[A-Za-z0-9._~-]+$",
            }),
          },
          { additionalProperties: true },
        ),
        body: AnalysisRunCreateSchema,
        response: {
          202: AnalysisRunSchema,
          404: ProblemSchema,
          409: ProblemSchema,
          ...protectedErrors,
        },
      }),
    },
    async (request, reply) => {
      const header = request.headers["idempotency-key"];
      const key = Array.isArray(header) ? header[0] : header;
      if (!key) {
        throw new ApiProblem(422, "Request validation failed", "Idempotency-Key is required.", "validation");
      }
      const { run, replay } = store.createRun(
        principal(request),
        key,
        request.body as AnalysisRunCreate,
      );
      return reply
        .code(202)
        .header("Location", `/analysis-runs/${run.id}`)
        .header("Retry-After", "1")
        .header("Idempotent-Replay", replay ? "true" : "false")
        .send(run);
    },
  );

  app.get(
    "/analysis-runs/:runId",
    {
      preHandler: requireScopes("runs:read"),
      schema: schema({
        operationId: "getAnalysisRun",
        tags: ["Analysis Runs"],
        summary: "Retrieve an analysis run",
        params: RunIdParams,
        response: { 200: AnalysisRunSchema, 404: ProblemSchema, ...protectedErrors },
      }),
    },
    async (request) => {
      const { runId } = request.params as { runId: string };
      return store.getRun(runId, principal(request));
    },
  );

  app.post(
    "/analysis-runs/:runId/cancellation",
    {
      preHandler: requireScopes("runs:write"),
      schema: schema({
        operationId: "cancelAnalysisRun",
        tags: ["Analysis Runs"],
        summary: "Cancel an analysis run",
        params: RunIdParams,
        response: {
          200: AnalysisRunSchema,
          404: ProblemSchema,
          409: ProblemSchema,
          ...protectedErrors,
        },
      }),
    },
    async (request) => {
      const { runId } = request.params as { runId: string };
      return store.cancelRun(runId, principal(request));
    },
  );

  app.get(
    "/analysis-runs/:runId/artifacts",
    {
      preHandler: requireScopes("artifacts:read"),
      schema: schema({
        operationId: "listRunArtifacts",
        tags: ["Artifacts"],
        summary: "List run artifacts",
        params: RunIdParams,
        response: {
          200: ArtifactPageSchema,
          404: ProblemSchema,
          409: ProblemSchema,
          ...protectedErrors,
        },
      }),
    },
    async (request) => {
      const { runId } = request.params as { runId: string };
      return { items: store.listArtifacts(runId, principal(request)) };
    },
  );

  app.get(
    "/analysis-runs/:runId/events",
    {
      preHandler: requireScopes("runs:read"),
      schema: schema({
        operationId: "streamAnalysisRunEvents",
        tags: ["Analysis Runs"],
        summary: "Stream analysis progress",
        params: RunIdParams,
        response: { 404: ProblemSchema, ...protectedErrors },
      }),
    },
    async (request, reply) => {
      const { runId } = request.params as { runId: string };
      const actor = principal(request);
      const accept = request.headers.accept ?? "text/event-stream";

      async function* observe(): AsyncGenerator<string> {
        let emitted = 0;
        for (let attempt = 0; attempt < 250; attempt += 1) {
          const events = store.progressEvents(runId, actor);
          for (const event of events.slice(emitted)) {
            emitted += 1;
            if (accept.includes("application/x-ndjson")) {
              yield `${JSON.stringify(event)}\n`;
            } else {
              yield (
                `id: ${event.eventId}\n` +
                "event: progress\n" +
                `data: ${JSON.stringify(event)}\n\n`
              );
            }
          }
          const current = store.getRun(runId, actor);
          if (["completed", "failed", "canceled"].includes(current.status)) {
            return;
          }
          await new Promise((resolve) => setTimeout(resolve, 10));
        }
      }

      if (accept.includes("application/x-ndjson")) {
        return reply
          .type("application/x-ndjson")
          .send(Readable.from(observe()));
      }
      return reply
        .header("Cache-Control", "no-cache")
        .type("text/event-stream")
        .send(Readable.from(observe()));
    },
  );

  app.get(
    "/artifacts/:artifactId",
    {
      preHandler: requireScopes("artifacts:read"),
      schema: schema({
        operationId: "getArtifact",
        tags: ["Artifacts"],
        summary: "Retrieve artifact metadata",
        params: ArtifactIdParams,
        response: { 200: ArtifactSchema, 404: ProblemSchema, ...protectedErrors },
      }),
    },
    async (request) => {
      const { artifactId } = request.params as { artifactId: string };
      return store.getArtifact(artifactId, principal(request));
    },
  );

  app.post(
    "/webhook-subscriptions",
    {
      preHandler: requireScopes("webhooks:write"),
      schema: schema({
        operationId: "createWebhookSubscription",
        tags: ["Webhooks"],
        summary: "Create a webhook subscription",
        body: WebhookSubscriptionCreateSchema,
        response: { 201: WebhookSubscriptionSchema, ...protectedErrors },
      }),
    },
    async (request, reply) => {
      const subscription = store.createSubscription(
        principal(request),
        request.body as WebhookSubscriptionCreate,
      );
      return reply
        .code(201)
        .header("Location", `/webhook-subscriptions/${subscription.id}`)
        .send(subscription);
    },
  );

  app.get(
    "/internal/diagnostics",
    {
      preHandler: requireScopes("admin"),
      schema: schema({
        operationId: "getInternalDiagnostics",
        tags: ["Internal"],
        summary: "Inspect deterministic training state",
        response: { 200: DiagnosticsSchema, ...protectedErrors },
      }),
    },
    async (request) => {
      principal(request);
      return store.diagnostics();
    },
  );

  return app;
}
