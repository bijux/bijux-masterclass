import { Type, type TSchema } from "@sinclair/typebox";

const Identifier = {
  project: Type.String({ pattern: "^prj_[0-9]{4,18}$" }),
  dataset: Type.String({ pattern: "^dts_[0-9]{4,18}$" }),
  run: Type.String({ pattern: "^run_[0-9]{4,18}$" }),
  artifact: Type.String({ pattern: "^art_[0-9]{4,18}$" }),
};

const OwnerId = Type.String({ pattern: "^[a-z][a-z0-9-]{2,31}$" });
const DateTime = Type.String({ format: "date-time" });
const Nullable = <T extends TSchema>(schema: T) => Type.Union([schema, Type.Null()]);

export const HealthSchema = Type.Object(
  {
    status: Type.Literal("ok"),
    service: Type.Literal("analysis-runs-api"),
    version: Type.String({ pattern: "^[0-9]+\\.[0-9]+\\.[0-9]+$" }),
    time: DateTime,
  },
  { additionalProperties: false },
);

export const ProjectCreateSchema = Type.Object(
  {
    name: Type.String({ minLength: 1, maxLength: 80, pattern: "^\\S(?:.*\\S)?$" }),
    description: Type.Optional(Type.String({ maxLength: 500 })),
  },
  { additionalProperties: false },
);

export const ProjectPatchSchema = Type.Object(
  {
    name: Type.Optional(Type.String({ minLength: 1, maxLength: 80, pattern: "^\\S(?:.*\\S)?$" })),
    description: Type.Optional(Nullable(Type.String({ maxLength: 500 }))),
  },
  { additionalProperties: false, minProperties: 1 },
);

export const ProjectSchema = Type.Object(
  {
    id: Identifier.project,
    ownerId: OwnerId,
    name: Type.String({ minLength: 1, maxLength: 80 }),
    description: Nullable(Type.String({ maxLength: 500 })),
    version: Type.Integer({ minimum: 1 }),
    createdAt: DateTime,
    updatedAt: DateTime,
  },
  { additionalProperties: false },
);

export const ProjectPageSchema = Type.Object(
  {
    items: Type.Array(ProjectSchema, { maxItems: 50 }),
    nextCursor: Nullable(Type.String({ pattern: "^[0-9]+$" })),
  },
  { additionalProperties: false },
);

export const LocalFileSourceSchema = Type.Object(
  {
    kind: Type.Literal("local-file"),
    fileName: Type.String({ minLength: 1, maxLength: 255 }),
    mediaType: Type.Union([
      Type.Literal("text/csv"),
      Type.Literal("application/json"),
      Type.Literal("application/octet-stream"),
    ]),
  },
  { additionalProperties: false },
);

export const RemoteObjectSourceSchema = Type.Object(
  {
    kind: Type.Literal("remote-object"),
    uri: Type.String({
      format: "uri",
      pattern: "^https://objects\\.example\\.test/[^?#\\s]+$",
    }),
    checksumSha256: Type.Optional(Type.String({ pattern: "^[a-f0-9]{64}$" })),
  },
  { additionalProperties: false },
);

export const DatasetSourceSchema = Type.Union([LocalFileSourceSchema, RemoteObjectSourceSchema]);

export const DatasetCreateSchema = Type.Object(
  {
    name: Type.String({ minLength: 1, maxLength: 100 }),
    source: DatasetSourceSchema,
  },
  { additionalProperties: false },
);

export const DatasetSchema = Type.Object(
  {
    id: Identifier.dataset,
    projectId: Identifier.project,
    ownerId: OwnerId,
    name: Type.String({ minLength: 1, maxLength: 100 }),
    source: DatasetSourceSchema,
    status: Type.Union([
      Type.Literal("awaiting-upload"),
      Type.Literal("ready"),
      Type.Literal("deleted"),
    ]),
    contentLength: Nullable(Type.Integer({ minimum: 0 })),
    checksumSha256: Nullable(Type.String({ pattern: "^[a-f0-9]{64}$" })),
    createdAt: DateTime,
    updatedAt: DateTime,
  },
  { additionalProperties: false },
);

export const DatasetPageSchema = Type.Object(
  {
    items: Type.Array(DatasetSchema, { maxItems: 50 }),
    nextCursor: Nullable(Type.String({ pattern: "^[0-9]+$" })),
  },
  { additionalProperties: false },
);

export const UploadReceiptSchema = Type.Object(
  {
    datasetId: Identifier.dataset,
    contentLength: Type.Integer({ minimum: 1, maximum: 1_048_576 }),
    checksumSha256: Type.String({ pattern: "^[a-f0-9]{64}$" }),
    uploadedAt: DateTime,
  },
  { additionalProperties: false },
);

export const AnalysisParametersSchema = Type.Object(
  {
    algorithm: Type.Union([
      Type.Literal("quality-summary"),
      Type.Literal("line-count"),
      Type.Literal("checksum"),
    ]),
    priority: Type.Optional(Type.Union([Type.Literal("normal"), Type.Literal("high")])),
    labels: Type.Optional(
      Type.Record(
        Type.String({ pattern: "^[a-z][a-z0-9_.-]{0,31}$" }),
        Type.String({ maxLength: 80 }),
        { maxProperties: 10 },
      ),
    ),
  },
  { additionalProperties: false },
);

export const AnalysisRunCreateSchema = Type.Object(
  {
    projectId: Identifier.project,
    datasetId: Identifier.dataset,
    parameters: AnalysisParametersSchema,
    callbackUrl: Type.Optional(
      Type.String({
        format: "uri",
        pattern: "^https://hooks\\.example\\.test(?:/[^#\\s]*)?$",
      }),
    ),
  },
  { additionalProperties: false },
);

export const AnalysisRunSchema = Type.Object(
  {
    id: Identifier.run,
    projectId: Identifier.project,
    datasetId: Identifier.dataset,
    ownerId: OwnerId,
    status: Type.Union([
      Type.Literal("queued"),
      Type.Literal("running"),
      Type.Literal("completed"),
      Type.Literal("failed"),
      Type.Literal("canceled"),
    ]),
    parameters: Type.Object(
      {
        algorithm: Type.Union([
          Type.Literal("quality-summary"),
          Type.Literal("line-count"),
          Type.Literal("checksum"),
        ]),
        priority: Type.Union([Type.Literal("normal"), Type.Literal("high")]),
        labels: Type.Record(Type.String(), Type.String({ maxLength: 80 }), { maxProperties: 10 }),
      },
      { additionalProperties: false },
    ),
    progress: Type.Integer({ minimum: 0, maximum: 100 }),
    createdAt: DateTime,
    updatedAt: DateTime,
    completedAt: Nullable(DateTime),
    artifactIds: Type.Array(Identifier.artifact, { maxItems: 10 }),
  },
  { additionalProperties: false },
);

export const AnalysisRunPageSchema = Type.Object(
  {
    items: Type.Array(AnalysisRunSchema, { maxItems: 50 }),
    nextCursor: Nullable(Type.String({ pattern: "^[0-9]+$" })),
  },
  { additionalProperties: false },
);

export const ArtifactSchema = Type.Object(
  {
    id: Identifier.artifact,
    runId: Identifier.run,
    ownerId: OwnerId,
    name: Type.String({ minLength: 1, maxLength: 120 }),
    mediaType: Type.Union([Type.Literal("application/json"), Type.Literal("text/plain")]),
    size: Type.Integer({ minimum: 1 }),
    checksumSha256: Type.String({ pattern: "^[a-f0-9]{64}$" }),
    createdAt: DateTime,
  },
  { additionalProperties: false },
);

export const ArtifactPageSchema = Type.Object(
  { items: Type.Array(ArtifactSchema, { maxItems: 10 }) },
  { additionalProperties: false },
);

export const WebhookSubscriptionCreateSchema = Type.Object(
  {
    targetUrl: Type.String({
      format: "uri",
      pattern: "^https://hooks\\.example\\.test(?:/[^#\\s]*)?$",
    }),
    eventTypes: Type.Array(
      Type.Union([Type.Literal("analysis.completed"), Type.Literal("analysis.failed")]),
      { minItems: 1, maxItems: 2, uniqueItems: true },
    ),
    secret: Type.String({ minLength: 16, maxLength: 128 }),
  },
  { additionalProperties: false },
);

export const WebhookSubscriptionSchema = Type.Object(
  {
    id: Type.String({ pattern: "^whs_[0-9]{4,18}$" }),
    ownerId: OwnerId,
    targetUrl: Type.String({
      format: "uri",
      pattern: "^https://hooks\\.example\\.test(?:/[^#\\s]*)?$",
    }),
    eventTypes: Type.Array(
      Type.Union([Type.Literal("analysis.completed"), Type.Literal("analysis.failed")]),
      { minItems: 1, maxItems: 2, uniqueItems: true },
    ),
    secretHint: Type.String({ pattern: "^\\*{4}.{4}$" }),
    createdAt: DateTime,
  },
  { additionalProperties: false },
);

export const RunProgressEventSchema = Type.Object(
  {
    eventId: Type.String({ pattern: "^evt_[0-9]{4,18}$" }),
    runId: Identifier.run,
    status: AnalysisRunSchema.properties.status,
    progress: Type.Integer({ minimum: 0, maximum: 100 }),
    occurredAt: DateTime,
  },
  { additionalProperties: false },
);

export const RunCompletedEventSchema = Type.Object(
  {
    eventId: Type.String({ pattern: "^evt_[0-9]{4,18}$" }),
    eventType: Type.Literal("analysis.completed"),
    occurredAt: DateTime,
    run: AnalysisRunSchema,
  },
  { additionalProperties: false },
);

export const DiagnosticsSchema = Type.Object(
  {
    counts: Type.Object(
      {
        projects: Type.Integer({ minimum: 0 }),
        datasets: Type.Integer({ minimum: 0 }),
        runs: Type.Integer({ minimum: 0 }),
        artifacts: Type.Integer({ minimum: 0 }),
        subscriptions: Type.Integer({ minimum: 0 }),
      },
      { additionalProperties: false },
    ),
    outboundEvents: Type.Array(RunCompletedEventSchema),
  },
  { additionalProperties: false },
);

export const ValidationIssueSchema = Type.Object(
  {
    location: Type.Array(Type.Union([Type.String(), Type.Integer()]), { minItems: 1 }),
    message: Type.String({ minLength: 1, maxLength: 300 }),
    code: Type.String({ minLength: 1, maxLength: 80 }),
  },
  { additionalProperties: false },
);

export const ProblemSchema = Type.Object(
  {
    type: Type.String(),
    title: Type.String(),
    status: Type.Integer({ minimum: 400, maximum: 599 }),
    detail: Type.String(),
    instance: Type.String(),
    requestId: Type.String({ pattern: "^req_[a-f0-9]{12}$" }),
  },
  { additionalProperties: true },
);

export const ValidationProblemSchema = Type.Object(
  {
    type: Type.String(),
    title: Type.String(),
    status: Type.Literal(422),
    detail: Type.String(),
    instance: Type.String(),
    requestId: Type.String({ pattern: "^req_[a-f0-9]{12}$" }),
    errors: Type.Array(ValidationIssueSchema, { minItems: 1 }),
  },
  { additionalProperties: false },
);

export const ProjectIdParams = Type.Object({ projectId: Identifier.project });
export const DatasetIdParams = Type.Object({ datasetId: Identifier.dataset });
export const RunIdParams = Type.Object({ runId: Identifier.run });
export const ArtifactIdParams = Type.Object({ artifactId: Identifier.artifact });

export const PageQuery = Type.Object(
  {
    limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 50, default: 20 })),
    cursor: Type.Optional(Type.String({ pattern: "^[0-9]+$" })),
  },
  { additionalProperties: false },
);
