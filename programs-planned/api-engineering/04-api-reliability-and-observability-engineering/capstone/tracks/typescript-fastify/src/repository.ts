import type { PoolClient } from "pg";

import { Database, type Row } from "./db.js";
import {
  filterFingerprint,
  parseProjectEtag,
  requestFingerprint,
  retryDelaySeconds,
} from "./domain.js";
import { ApiProblem } from "./problems.js";
import type {
  AnalysisRunCreate,
  Artifact,
  ClaimedDelivery,
  ClaimedJob,
  Dataset,
  DatasetCreate,
  DatasetSource,
  Principal,
  Project,
  ProjectCreate,
  ProjectPatch,
  ResultSummary,
  StagedFile,
  RunProgressEvent,
  RunRepresentation,
  WebhookSubscription,
  WebhookSubscriptionCreate,
} from "./types.js";

export type StoredResponse = Readonly<{
  status: number;
  headers: Record<string, string>;
  body: RunRepresentation;
  replay: boolean;
}>;

type CursorWindow = Readonly<{
  // node-postgres returns PostgreSQL bigint values as strings. Keep them as
  // strings so a long-lived service never crosses JavaScript's 53-bit limit.
  boundary: string;
  snapshot: string;
}>;

type Page<T> = Readonly<{
  items: T[];
  nextCursor: string | null;
}>;

function iso(value: unknown): string {
  if (value instanceof Date) return value.toISOString();
  return String(value);
}

function notFound(resource: string): ApiProblem {
  return new ApiProblem(
    404,
    "Resource not found",
    `The requested ${resource} does not exist.`,
    "not-found",
  );
}

/**
 * PostgreSQL adapter for application and worker use cases.
 *
 * One adapter intentionally owns transactions that cross runs, jobs,
 * artifacts, events, and outbox rows. Splitting those operations into one
 * repository per table would conceal the atomicity boundary this course is
 * teaching.
 */
export class PostgresRepository {
  public constructor(
    private readonly database: Database,
    private readonly encryptionKey: string,
    private readonly callbackSecret: string,
    private readonly serviceRelease: "1.0" | "1.1",
  ) {}

  public get exposesApi12(): boolean {
    return this.serviceRelease === "1.1";
  }

  public async health(): Promise<void> {
    await this.database.health();
  }

  public async close(): Promise<void> {
    await this.database.close();
  }

  // -----------------------------------------------------------------------
  // Driver-row mapping
  // -----------------------------------------------------------------------
  private project(row: Row): Project {
    return {
      id: row.id,
      ownerId: row.owner_id,
      name: row.name,
      description: row.description,
      version: Number(row.version),
      createdAt: iso(row.created_at),
      updatedAt: iso(row.updated_at),
    };
  }

  private dataset(row: Row): Dataset {
    return {
      id: row.id,
      projectId: row.project_id,
      ownerId: row.owner_id,
      name: row.name,
      source: row.source as DatasetSource,
      status: row.status,
      contentLength:
        row.content_length === null ? null : Number(row.content_length),
      checksumSha256: row.checksum_sha256,
      createdAt: iso(row.created_at),
      updatedAt: iso(row.updated_at),
    };
  }

  private run(row: Row): RunRepresentation {
    const common = {
      id: row.id,
      projectId: row.project_id,
      datasetId: row.dataset_id,
      ownerId: row.owner_id,
      status: row.status,
      parameters: row.parameters,
      progress: Number(row.progress),
      createdAt: iso(row.created_at),
      updatedAt: iso(row.updated_at),
      completedAt: row.completed_at ? iso(row.completed_at) : null,
      artifactIds: (row.artifact_ids ?? []) as string[],
    };
    if (!this.exposesApi12) return common;
    return {
      ...common,
      resultSummary: (row.result_summary ?? null) as ResultSummary | null,
    };
  }

  private artifact(row: Row): Artifact {
    return {
      id: row.id,
      runId: row.run_id,
      ownerId: row.owner_id,
      name: row.name,
      mediaType: row.media_type,
      size: Number(row.size),
      checksumSha256: row.checksum_sha256,
      createdAt: iso(row.created_at),
    };
  }

  private runSelect(): string {
    return `
      SELECT
        r.*,
        COALESCE(
          (
            SELECT array_agg(a.id ORDER BY a.position)
            FROM artifacts AS a
            WHERE a.run_id = r.id
          ),
          '{}'::text[]
        ) AS artifact_ids
      FROM analysis_runs AS r
    `;
  }

  // -----------------------------------------------------------------------
  // Opaque, principal-bound, filter-bound, high-water cursors
  // -----------------------------------------------------------------------
  private async cursorWindow(
    client: PoolClient,
    principal: Principal,
    operationId: string,
    handle: string | undefined,
    filters: unknown,
    snapshotSql: string,
    snapshotArguments: unknown[],
  ): Promise<CursorWindow> {
    if (handle === undefined) {
      const result = await client.query(snapshotSql, snapshotArguments);
      return {
        boundary: "0",
        snapshot: String(result.rows[0]?.snapshot_position ?? "0"),
      };
    }

    const fingerprint = filterFingerprint(
      operationId,
      principal.subject,
      filters,
    );
    const result = await client.query(
      `
        SELECT boundary_position, snapshot_position
        FROM pagination_cursors
        WHERE handle = $1
          AND owner_id = $2
          AND operation_id = $3
          AND filter_fingerprint = $4
          AND expires_at > clock_timestamp()
      `,
      [handle, principal.subject, operationId, fingerprint],
    );
    if (!(result.rowCount ?? 0)) {
      throw new ApiProblem(
        422,
        "Request validation failed",
        "The cursor is invalid, expired, or belongs to another query.",
        "cursor-invalid",
      );
    }
    return {
      boundary: String(result.rows[0]?.boundary_position),
      snapshot: String(result.rows[0]?.snapshot_position),
    };
  }

  private async newCursor(
    client: PoolClient,
    principal: Principal,
    operationId: string,
    filters: unknown,
    boundary: string,
    snapshot: string,
  ): Promise<string> {
    await client.query(
      "DELETE FROM pagination_cursors WHERE expires_at <= clock_timestamp()",
    );
    const result = await client.query(
      `
        INSERT INTO pagination_cursors(
          owner_id,
          operation_id,
          filter_fingerprint,
          boundary_position,
          snapshot_position
        )
        VALUES ($1, $2, $3, $4, $5)
        RETURNING handle
      `,
      [
        principal.subject,
        operationId,
        filterFingerprint(operationId, principal.subject, filters),
        boundary,
        snapshot,
      ],
    );
    return String(result.rows[0]?.handle);
  }

  private async page<T>(
    client: PoolClient,
    principal: Principal,
    operationId: string,
    filters: unknown,
    rows: Row[],
    limit: number,
    snapshot: string,
    map: (row: Row) => T,
  ): Promise<Page<T>> {
    const visible = rows.slice(0, limit);
    const nextCursor =
      rows.length > limit
        ? await this.newCursor(
            client,
            principal,
            operationId,
            filters,
            String(visible.at(-1)!.position),
            snapshot,
          )
        : null;
    return { items: visible.map(map), nextCursor };
  }

  // -----------------------------------------------------------------------
  // Projects
  // -----------------------------------------------------------------------
  public async createProject(
    principal: Principal,
    body: ProjectCreate,
  ): Promise<Project> {
    const result = await this.database.pool.query(
      `
        INSERT INTO projects(owner_id, name, description)
        VALUES ($1, $2, $3)
        RETURNING *
      `,
      [principal.subject, body.name, body.description ?? null],
    );
    return this.project(result.rows[0] as Row);
  }

  public async getProject(
    principal: Principal,
    projectId: string,
  ): Promise<Project> {
    const result = await this.database.pool.query(
      `
        SELECT *
        FROM projects
        WHERE id = $1 AND ($2 OR owner_id = $3)
      `,
      [projectId, principal.admin, principal.subject],
    );
    if (!(result.rowCount ?? 0)) throw notFound("project");
    return this.project(result.rows[0] as Row);
  }

  public async listProjects(
    principal: Principal,
    limit: number,
    cursor: string | undefined,
    name: string | undefined,
  ): Promise<Page<Project>> {
    return this.database.transaction(async (client) => {
      const operationId = "listProjects";
      const filters = { name: name ?? null };
      const values: unknown[] = [principal.admin, principal.subject];
      const predicates = ["($1 OR owner_id = $2)"];
      if (name !== undefined) {
        values.push(`%${name}%`);
        predicates.push(`lower(name) LIKE lower($${values.length})`);
      }

      const window = await this.cursorWindow(
        client,
        principal,
        operationId,
        cursor,
        filters,
        `
          SELECT COALESCE(max(position), 0) AS snapshot_position
          FROM projects
          WHERE ${predicates.join(" AND ")}
        `,
        values,
      );
      const queryValues = [...values, window.boundary, window.snapshot, limit + 1];
      const result = await client.query(
        `
          SELECT *
          FROM projects
          WHERE ${predicates.join(" AND ")}
            AND position > $${values.length + 1}
            AND position <= $${values.length + 2}
          ORDER BY position
          LIMIT $${values.length + 3}
        `,
        queryValues,
      );
      return this.page(
        client,
        principal,
        operationId,
        filters,
        result.rows as Row[],
        limit,
        window.snapshot,
        (row) => this.project(row),
      );
    });
  }

  public async updateProject(
    principal: Principal,
    projectId: string,
    ifMatch: string | undefined,
    body: ProjectPatch,
  ): Promise<Project> {
    if (!ifMatch) {
      throw new ApiProblem(
        428,
        "Precondition required",
        "This update requires the latest If-Match entity tag.",
        "precondition-required",
      );
    }

    let expectedVersion: number;
    try {
      expectedVersion = parseProjectEtag(ifMatch, projectId);
    } catch {
      throw new ApiProblem(
        412,
        "Precondition failed",
        "The supplied entity tag is malformed or belongs to another resource.",
        "precondition-failed",
      );
    }

    return this.database.transaction(async (client) => {
      const current = await client.query(
        `
          SELECT name, description
          FROM projects
          WHERE id = $1 AND ($2 OR owner_id = $3)
        `,
        [projectId, principal.admin, principal.subject],
      );
      if (!(current.rowCount ?? 0)) throw notFound("project");

      const row = current.rows[0] as Row;
      const name = Object.hasOwn(body, "name") ? body.name : row.name;
      const description = Object.hasOwn(body, "description")
        ? body.description
        : row.description;
      const updated = await client.query(
        `
          UPDATE projects
          SET name = $1,
              description = $2,
              version = version + 1,
              updated_at = clock_timestamp()
          WHERE id = $3
            AND ($4 OR owner_id = $5)
            AND version = $6
          RETURNING *
        `,
        [
          name,
          description,
          projectId,
          principal.admin,
          principal.subject,
          expectedVersion,
        ],
      );
      if (!(updated.rowCount ?? 0)) {
        throw new ApiProblem(
          412,
          "Precondition failed",
          "The project changed concurrently.",
          "precondition-failed",
        );
      }
      return this.project(updated.rows[0] as Row);
    });
  }

  // -----------------------------------------------------------------------
  // Datasets
  // -----------------------------------------------------------------------
  public async createDataset(
    principal: Principal,
    projectId: string,
    body: DatasetCreate,
  ): Promise<Dataset> {
    const sourceKind = body.source.kind;
    const status = sourceKind === "local-file" ? "awaiting-upload" : "ready";
    const checksum =
      sourceKind === "remote-object"
        ? body.source.checksumSha256 ?? null
        : null;
    const result = await this.database.pool.query(
      `
        INSERT INTO datasets(
          project_id,
          owner_id,
          name,
          source_kind,
          source,
          status,
          checksum_sha256
        )
        SELECT id, owner_id, $1, $2, $3::jsonb, $4, $5
        FROM projects
        WHERE id = $6 AND ($7 OR owner_id = $8)
        RETURNING *
      `,
      [
        body.name,
        sourceKind,
        JSON.stringify(body.source),
        status,
        checksum,
        projectId,
        principal.admin,
        principal.subject,
      ],
    );
    if (!(result.rowCount ?? 0)) throw notFound("project");
    return this.dataset(result.rows[0] as Row);
  }

  public async getDataset(
    principal: Principal,
    datasetId: string,
  ): Promise<Dataset> {
    const result = await this.database.pool.query(
      `
        SELECT *
        FROM datasets
        WHERE id = $1
          AND status <> 'deleted'
          AND ($2 OR owner_id = $3)
      `,
      [datasetId, principal.admin, principal.subject],
    );
    if (!(result.rowCount ?? 0)) throw notFound("dataset");
    return this.dataset(result.rows[0] as Row);
  }

  public async listDatasets(
    principal: Principal,
    projectId: string,
    limit: number,
    cursor: string | undefined,
    status: string | undefined,
  ): Promise<Page<Dataset>> {
    return this.database.transaction(async (client) => {
      const project = await client.query(
        `
          SELECT 1
          FROM projects
          WHERE id = $1 AND ($2 OR owner_id = $3)
        `,
        [projectId, principal.admin, principal.subject],
      );
      if (!(project.rowCount ?? 0)) throw notFound("project");

      const operationId = "listProjectDatasets";
      const filters = { projectId, status: status ?? null };
      const values: unknown[] = [
        projectId,
        principal.admin,
        principal.subject,
      ];
      const predicates = [
        "project_id = $1",
        "($2 OR owner_id = $3)",
        "status <> 'deleted'",
      ];
      if (status !== undefined) {
        values.push(status);
        predicates.push(`status = $${values.length}`);
      }

      const window = await this.cursorWindow(
        client,
        principal,
        operationId,
        cursor,
        filters,
        `
          SELECT COALESCE(max(position), 0) AS snapshot_position
          FROM datasets
          WHERE ${predicates.join(" AND ")}
        `,
        values,
      );
      const result = await client.query(
        `
          SELECT *
          FROM datasets
          WHERE ${predicates.join(" AND ")}
            AND position > $${values.length + 1}
            AND position <= $${values.length + 2}
          ORDER BY position
          LIMIT $${values.length + 3}
        `,
        [...values, window.boundary, window.snapshot, limit + 1],
      );
      return this.page(
        client,
        principal,
        operationId,
        filters,
        result.rows as Row[],
        limit,
        window.snapshot,
        (row) => this.dataset(row),
      );
    });
  }

  public async attachUploadedContent(
    principal: Principal,
    datasetId: string,
    file: StagedFile,
    storageKey: string,
  ): Promise<{
    datasetId: string;
    contentLength: number;
    checksumSha256: string;
    uploadedAt: string;
  }> {
    return this.database.transaction(async (client) => {
      const result = await client.query(
        `
          SELECT *
          FROM datasets
          WHERE id = $1
            AND status <> 'deleted'
            AND ($2 OR owner_id = $3)
          FOR UPDATE
        `,
        [datasetId, principal.admin, principal.subject],
      );
      if (!(result.rowCount ?? 0)) throw notFound("dataset");
      const row = result.rows[0] as Row;
      if (row.source_kind !== "local-file") {
        throw new ApiProblem(
          409,
          "Request conflict",
          "Remote-object datasets do not accept local uploads.",
          "conflict",
        );
      }
      if (row.status === "ready") {
        if (row.checksum_sha256 === file.checksumSha256) {
          return {
            datasetId,
            contentLength: Number(row.content_length),
            checksumSha256: row.checksum_sha256,
            uploadedAt: iso(row.updated_at),
          };
        }
        throw new ApiProblem(
          409,
          "Request conflict",
          "This dataset already has different content.",
          "conflict",
        );
      }

      const updated = await client.query(
        `
          UPDATE datasets
          SET status = 'ready',
              content_path = $1,
              content_length = $2,
              checksum_sha256 = $3,
              updated_at = clock_timestamp()
          WHERE position = $4
          RETURNING *
        `,
        [storageKey, file.size, file.checksumSha256, row.position],
      );
      return {
        datasetId,
        contentLength: file.size,
        checksumSha256: file.checksumSha256,
        uploadedAt: iso(updated.rows[0]?.updated_at),
      };
    });
  }

  public async deleteDataset(
    principal: Principal,
    datasetId: string,
  ): Promise<void> {
    await this.database.transaction(async (client) => {
      const dataset = await client.query(
        `
          SELECT *
          FROM datasets
          WHERE id = $1
            AND status <> 'deleted'
            AND ($2 OR owner_id = $3)
          FOR UPDATE
        `,
        [datasetId, principal.admin, principal.subject],
      );
      if (!(dataset.rowCount ?? 0)) throw notFound("dataset");
      const activeRun = await client.query(
        `
          SELECT 1
          FROM analysis_runs
          WHERE dataset_id = $1 AND status IN ('queued', 'running')
          LIMIT 1
        `,
        [datasetId],
      );
      if (activeRun.rowCount ?? 0) {
        throw new ApiProblem(
          409,
          "Request conflict",
          "An active analysis run depends on this dataset.",
          "conflict",
        );
      }
      await client.query(
        `
          UPDATE datasets
          SET status = 'deleted',
              deleted_at = clock_timestamp(),
              updated_at = clock_timestamp()
          WHERE id = $1
        `,
        [datasetId],
      );
    });
  }

  // -----------------------------------------------------------------------
  // Analysis runs and persistent idempotency
  // -----------------------------------------------------------------------
  public async createRunIdempotently(
    principal: Principal,
    idempotencyKey: string,
    body: AnalysisRunCreate,
  ): Promise<StoredResponse> {
    const operationId = "createAnalysisRun";
    const normalizedParameters = {
      algorithm: body.parameters.algorithm,
      priority: body.parameters.priority ?? "normal",
      labels: body.parameters.labels ?? {},
    };
    const normalizedBody = {
      projectId: body.projectId,
      datasetId: body.datasetId,
      parameters: normalizedParameters,
      ...(body.callbackUrl === undefined
        ? {}
        : { callbackUrl: body.callbackUrl }),
    };
    const fingerprint = requestFingerprint(
      operationId,
      principal.subject,
      normalizedBody,
    );

    return this.database.transaction(async (client) => {
      await client.query(
        `
          INSERT INTO idempotency_records(
            owner_id,
            operation_id,
            idempotency_key,
            request_fingerprint,
            state
          )
          VALUES ($1, $2, $3, $4, 'processing')
          ON CONFLICT DO NOTHING
        `,
        [principal.subject, operationId, idempotencyKey, fingerprint],
      );
      const records = await client.query(
        `
          SELECT *
          FROM idempotency_records
          WHERE owner_id = $1
            AND operation_id = $2
            AND idempotency_key = $3
          FOR UPDATE
        `,
        [principal.subject, operationId, idempotencyKey],
      );
      const record = records.rows[0] as Row;
      if (record.request_fingerprint !== fingerprint) {
        throw new ApiProblem(
          409,
          "Request conflict",
          "The idempotency key was already used with a different request body.",
          "idempotency-conflict",
        );
      }
      if (record.state === "completed") {
        return {
          status: Number(record.response_status),
          headers: record.response_headers as Record<string, string>,
          body: record.response_body as RunRepresentation,
          replay: true,
        };
      }

      const source = await client.query(
        `
          SELECT
            p.id AS project_id,
            p.owner_id,
            d.id AS dataset_id,
            d.status AS dataset_status
          FROM projects AS p
          JOIN datasets AS d
            ON d.project_id = p.id AND d.owner_id = p.owner_id
          WHERE p.id = $1
            AND d.id = $2
            AND ($3 OR p.owner_id = $4)
          FOR UPDATE OF d
        `,
        [
          body.projectId,
          body.datasetId,
          principal.admin,
          principal.subject,
        ],
      );
      if (!(source.rowCount ?? 0)) {
        throw notFound("project or dataset");
      }
      const durableSource = source.rows[0] as Row;
      if (durableSource.dataset_status !== "ready") {
        throw new ApiProblem(
          409,
          "Request conflict",
          "The dataset must be ready before analysis starts.",
          "conflict",
        );
      }

      const inserted = await client.query(
        `
          INSERT INTO analysis_runs(
            project_id,
            dataset_id,
            owner_id,
            status,
            parameters,
            callback_url,
            progress
          )
          VALUES ($1, $2, $3, 'queued', $4::jsonb, $5, 0)
          RETURNING *
        `,
        [
          durableSource.project_id,
          durableSource.dataset_id,
          durableSource.owner_id,
          JSON.stringify(normalizedParameters),
          body.callbackUrl ?? null,
        ],
      );
      const run = inserted.rows[0] as Row;
      await client.query(
        "INSERT INTO run_jobs(run_id, status) VALUES ($1, 'queued')",
        [run.id],
      );
      await this.insertRunEvent(
        client,
        run.id,
        run.owner_id,
        "queued",
        0,
      );

      const response = this.run({ ...run, artifact_ids: [] });
      const headers = {
        Location: `/analysis-runs/${run.id}`,
        "Retry-After": "1",
        "Idempotent-Replay": "false",
      };
      await client.query(
        `
          UPDATE idempotency_records
          SET state = 'completed',
              resource_id = $1,
              response_status = 202,
              response_headers = $2::jsonb,
              response_body = $3::jsonb,
              completed_at = clock_timestamp()
          WHERE owner_id = $4
            AND operation_id = $5
            AND idempotency_key = $6
        `,
        [
          run.id,
          JSON.stringify(headers),
          JSON.stringify(response),
          principal.subject,
          operationId,
          idempotencyKey,
        ],
      );
      return { status: 202, headers, body: response, replay: false };
    });
  }

  public async getRun(
    principal: Principal,
    runId: string,
  ): Promise<RunRepresentation> {
    const result = await this.database.pool.query(
      this.runSelect() +
        ` WHERE r.id = $1 AND ($2 OR r.owner_id = $3)`,
      [runId, principal.admin, principal.subject],
    );
    if (!(result.rowCount ?? 0)) throw notFound("analysis run");
    return this.run(result.rows[0] as Row);
  }

  public async listRuns(
    principal: Principal,
    limit: number,
    cursor: string | undefined,
    status: string | undefined,
  ): Promise<Page<RunRepresentation>> {
    return this.database.transaction(async (client) => {
      const operationId = "listAnalysisRuns";
      const filters = { status: status ?? null };
      const values: unknown[] = [principal.admin, principal.subject];
      const predicates = ["($1 OR r.owner_id = $2)"];
      if (status !== undefined) {
        values.push(status);
        predicates.push(`r.status = $${values.length}`);
      }

      const window = await this.cursorWindow(
        client,
        principal,
        operationId,
        cursor,
        filters,
        `
          SELECT COALESCE(max(r.position), 0) AS snapshot_position
          FROM analysis_runs AS r
          WHERE ${predicates.join(" AND ")}
        `,
        values,
      );
      const result = await client.query(
        this.runSelect() +
          `
            WHERE ${predicates.join(" AND ")}
              AND r.position > $${values.length + 1}
              AND r.position <= $${values.length + 2}
            ORDER BY r.position
            LIMIT $${values.length + 3}
          `,
        [...values, window.boundary, window.snapshot, limit + 1],
      );
      return this.page(
        client,
        principal,
        operationId,
        filters,
        result.rows as Row[],
        limit,
        window.snapshot,
        (row) => this.run(row),
      );
    });
  }

  public async cancelRun(
    principal: Principal,
    runId: string,
  ): Promise<RunRepresentation> {
    return this.database.transaction(async (client) => {
      const result = await client.query(
        `
          SELECT *
          FROM analysis_runs
          WHERE id = $1 AND ($2 OR owner_id = $3)
          FOR UPDATE
        `,
        [runId, principal.admin, principal.subject],
      );
      if (!(result.rowCount ?? 0)) throw notFound("analysis run");
      const row = result.rows[0] as Row;
      if (!(["queued", "running"] as string[]).includes(row.status)) {
        throw new ApiProblem(
          409,
          "Request conflict",
          "Only queued or running analysis can be canceled.",
          "invalid-run-transition",
        );
      }

      let updated: Row;
      if (row.status === "queued") {
        const changed = await client.query(
          `
            UPDATE analysis_runs
            SET status = 'canceled',
                cancellation_requested_at = clock_timestamp(),
                completed_at = clock_timestamp(),
                updated_at = clock_timestamp()
            WHERE position = $1
            RETURNING *
          `,
          [row.position],
        );
        updated = changed.rows[0] as Row;
        await client.query(
          `
            UPDATE run_jobs
            SET status = 'canceled',
                lease_owner = NULL,
                lease_expires_at = NULL,
                updated_at = clock_timestamp()
            WHERE run_id = $1
          `,
          [runId],
        );
        await this.insertRunEvent(
          client,
          runId,
          row.owner_id,
          "canceled",
          0,
        );
      } else {
        const changed = await client.query(
          `
            UPDATE analysis_runs
            SET cancellation_requested_at = COALESCE(
                  cancellation_requested_at,
                  clock_timestamp()
                ),
                updated_at = clock_timestamp()
            WHERE position = $1
            RETURNING *
          `,
          [row.position],
        );
        updated = changed.rows[0] as Row;
      }
      return this.run({ ...updated, artifact_ids: [] });
    });
  }

  // -----------------------------------------------------------------------
  // Artifacts, progress, and subscriptions
  // -----------------------------------------------------------------------
  public async listArtifacts(
    principal: Principal,
    runId: string,
  ): Promise<Artifact[]> {
    const visible = await this.database.pool.query(
      `
        SELECT 1
        FROM analysis_runs
        WHERE id = $1 AND ($2 OR owner_id = $3)
      `,
      [runId, principal.admin, principal.subject],
    );
    if (!(visible.rowCount ?? 0)) throw notFound("analysis run");

    const result = await this.database.pool.query(
      `
        SELECT a.*
        FROM artifacts AS a
        JOIN analysis_runs AS r ON r.id = a.run_id
        WHERE a.run_id = $1
          AND r.status = 'completed'
          AND ($2 OR r.owner_id = $3)
        ORDER BY a.position
      `,
      [runId, principal.admin, principal.subject],
    );
    return (result.rows as Row[]).map((row) => this.artifact(row));
  }

  public async getArtifact(
    principal: Principal,
    artifactId: string,
  ): Promise<Artifact> {
    const result = await this.database.pool.query(
      `
        SELECT a.*
        FROM artifacts AS a
        JOIN analysis_runs AS r ON r.id = a.run_id
        WHERE a.id = $1
          AND r.status = 'completed'
          AND ($2 OR a.owner_id = $3)
      `,
      [artifactId, principal.admin, principal.subject],
    );
    if (!(result.rowCount ?? 0)) throw notFound("artifact");
    return this.artifact(result.rows[0] as Row);
  }

  public async artifactStorageKey(
    principal: Principal,
    artifactId: string,
  ): Promise<string> {
    const result = await this.database.pool.query(
      `
        SELECT a.storage_key
        FROM artifacts AS a
        JOIN analysis_runs AS r ON r.id = a.run_id
        WHERE a.id = $1
          AND r.status = 'completed'
          AND ($2 OR a.owner_id = $3)
      `,
      [artifactId, principal.admin, principal.subject],
    );
    if (!(result.rowCount ?? 0)) throw notFound("artifact");
    return String(result.rows[0]?.storage_key);
  }

  public async progressEvents(
    principal: Principal,
    runId: string,
    afterPosition = "0",
  ): Promise<RunProgressEvent[]> {
    const visible = await this.database.pool.query(
      `
        SELECT 1
        FROM analysis_runs
        WHERE id = $1 AND ($2 OR owner_id = $3)
      `,
      [runId, principal.admin, principal.subject],
    );
    if (!(visible.rowCount ?? 0)) throw notFound("analysis run");

    const result = await this.database.pool.query(
      `
        SELECT e.*
        FROM run_events AS e
        JOIN analysis_runs AS r ON r.id = e.run_id
        WHERE e.run_id = $1
          AND e.position > $2
          AND ($3 OR r.owner_id = $4)
        ORDER BY e.position
      `,
      [runId, afterPosition, principal.admin, principal.subject],
    );
    return (result.rows as Row[]).map((row) => ({
      eventId: row.event_id,
      runId: row.run_id,
      status: row.status,
      progress: Number(row.progress),
      occurredAt: iso(row.occurred_at),
    }));
  }

  public async createSubscription(
    principal: Principal,
    body: WebhookSubscriptionCreate,
  ): Promise<WebhookSubscription> {
    const secretHint = `****${body.secret.slice(-4)}`;
    const result = await this.database.pool.query(
      `
        INSERT INTO webhook_subscriptions(
          owner_id,
          target_url,
          event_types,
          secret_ciphertext,
          secret_hint
        )
        VALUES ($1, $2, $3, pgp_sym_encrypt($4, $5), $6)
        RETURNING *
      `,
      [
        principal.subject,
        body.targetUrl,
        body.eventTypes,
        body.secret,
        this.encryptionKey,
        secretHint,
      ],
    );
    const row = result.rows[0] as Row;
    return {
      id: row.id,
      ownerId: row.owner_id,
      targetUrl: row.target_url,
      eventTypes: row.event_types,
      secretHint: row.secret_hint,
      createdAt: iso(row.created_at),
    };
  }

  public async diagnostics(): Promise<Record<string, unknown>> {
    const counts: Record<string, number> = {};
    const tables = [
      ["projects", "projects"],
      ["datasets", "datasets"],
      ["analysis_runs", "runs"],
      ["artifacts", "artifacts"],
      ["webhook_subscriptions", "subscriptions"],
    ] as const;
    for (const [table, key] of tables) {
      const result = await this.database.pool.query(
        `SELECT count(*) AS count FROM ${table}`,
      );
      counts[key] = Number(result.rows[0]?.count);
    }
    const events = await this.database.pool.query(
      `
        SELECT payload
        FROM outbox_events
        WHERE event_type = 'analysis.completed'
        ORDER BY position
      `,
    );
    return {
      counts,
      outboundEvents: (events.rows as Row[]).map((row) => row.payload),
    };
  }

  // -----------------------------------------------------------------------
  // Durable jobs and fencing
  // -----------------------------------------------------------------------
  public async claimJob(
    workerId: string,
    leaseSeconds: number,
  ): Promise<ClaimedJob | null> {
    return this.database.transaction(async (client) => {
      const result = await client.query(
        `
          WITH candidate AS (
            SELECT j.run_id
            FROM run_jobs AS j
            JOIN analysis_runs AS r ON r.id = j.run_id
            WHERE j.status = 'queued'
              AND j.available_at <= clock_timestamp()
              AND r.status = 'queued'
              AND r.cancellation_requested_at IS NULL
            ORDER BY
              (r.parameters->>'priority' = 'high') DESC,
              j.created_at
            FOR UPDATE OF j SKIP LOCKED
            LIMIT 1
          )
          UPDATE run_jobs AS j
          SET status = 'leased',
              lease_owner = $1,
              lease_expires_at = clock_timestamp()
                + ($2 || ' seconds')::interval,
              lease_generation = lease_generation + 1,
              attempts = attempts + 1,
              updated_at = clock_timestamp()
          FROM candidate AS c,
               analysis_runs AS r,
               datasets AS d
          WHERE j.run_id = c.run_id
            AND r.id = j.run_id
            AND d.id = r.dataset_id
          RETURNING
            j.run_id,
            r.dataset_id,
            r.owner_id,
            r.parameters->>'algorithm' AS algorithm,
            d.source_kind,
            d.source,
            d.content_path,
            d.checksum_sha256,
            j.attempts,
            j.lease_generation
        `,
        [workerId, leaseSeconds],
      );
      if (!(result.rowCount ?? 0)) return null;
      const row = result.rows[0] as Row;
      return {
        runId: row.run_id,
        datasetId: row.dataset_id,
        ownerId: row.owner_id,
        algorithm: row.algorithm,
        sourceKind: row.source_kind,
        source: row.source,
        contentPath: row.content_path,
        expectedChecksum: row.checksum_sha256,
        attempt: Number(row.attempts),
        leaseOwner: workerId,
        leaseGeneration: Number(row.lease_generation),
      };
    });
  }

  private async lockJob(
    client: PoolClient,
    job: ClaimedJob,
  ): Promise<Row> {
    const result = await client.query(
      `
        SELECT *
        FROM run_jobs
        WHERE run_id = $1
          AND status = 'leased'
          AND lease_owner = $2
          AND lease_generation = $3
          AND lease_expires_at > clock_timestamp()
        FOR UPDATE
      `,
      [job.runId, job.leaseOwner, job.leaseGeneration],
    );
    if (!(result.rowCount ?? 0)) {
      throw new Error(`lease-lost:${job.runId}`);
    }
    return result.rows[0] as Row;
  }

  public async markJobRunning(job: ClaimedJob): Promise<void> {
    await this.database.transaction(async (client) => {
      await this.lockJob(client, job);
      const changed = await client.query(
        `
          UPDATE analysis_runs
          SET status = 'running',
              progress = 10,
              updated_at = clock_timestamp()
          WHERE id = $1 AND status = 'queued'
          RETURNING id
        `,
        [job.runId],
      );
      if (!(changed.rowCount ?? 0)) {
        throw new Error(`lease-lost:${job.runId}`);
      }
      await this.insertRunEvent(
        client,
        job.runId,
        job.ownerId,
        "running",
        10,
      );
    });
  }

  public async renewJobLease(
    job: ClaimedJob,
    leaseSeconds: number,
  ): Promise<void> {
    const result = await this.database.pool.query(
      `
        UPDATE run_jobs
        SET lease_expires_at = clock_timestamp()
              + ($1 || ' seconds')::interval,
            updated_at = clock_timestamp()
        WHERE run_id = $2
          AND status = 'leased'
          AND lease_owner = $3
          AND lease_generation = $4
          AND lease_expires_at > clock_timestamp()
        RETURNING run_id
      `,
      [leaseSeconds, job.runId, job.leaseOwner, job.leaseGeneration],
    );
    if (!(result.rowCount ?? 0)) {
      throw new Error(`lease-lost:${job.runId}`);
    }
  }

  public async completeJob(
    job: ClaimedJob,
    file: StagedFile,
    storageKey: string,
    name: string,
    summary: ResultSummary,
  ): Promise<boolean> {
    return this.database.transaction(async (client) => {
      await this.lockJob(client, job);
      const runResult = await client.query(
        "SELECT * FROM analysis_runs WHERE id = $1 FOR UPDATE",
        [job.runId],
      );
      const run = runResult.rows[0] as Row;
      if (run.cancellation_requested_at) {
        await this.cancelLocked(client, job, run);
        return false;
      }
      if (run.status !== "running") {
        throw new Error(`lease-lost:${job.runId}`);
      }

      const existing = await client.query(
        `
          SELECT *
          FROM artifacts
          WHERE run_id = $1 AND name = $2
          FOR UPDATE
        `,
        [job.runId, name],
      );
      let artifact: Row;
      if (existing.rowCount ?? 0) {
        artifact = existing.rows[0] as Row;
        if (artifact.checksum_sha256 !== file.checksumSha256) {
          throw new Error("duplicate job produced different artifact bytes");
        }
      } else {
        const inserted = await client.query(
          `
            INSERT INTO artifacts(
              run_id,
              owner_id,
              name,
              media_type,
              size,
              checksum_sha256,
              storage_key
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING *
          `,
          [
            job.runId,
            job.ownerId,
            name,
            file.mediaType,
            file.size,
            file.checksumSha256,
            storageKey,
          ],
        );
        artifact = inserted.rows[0] as Row;
      }

      const finished = this.exposesApi12
        ? await client.query(
            `
              UPDATE analysis_runs
              SET status = 'completed',
                  progress = 100,
                  completed_at = clock_timestamp(),
                  updated_at = clock_timestamp(),
                  result_summary = $1::jsonb
              WHERE id = $2
              RETURNING *
            `,
            [JSON.stringify(summary), job.runId],
          )
        : await client.query(
            `
              UPDATE analysis_runs
              SET status = 'completed',
                  progress = 100,
                  completed_at = clock_timestamp(),
                  updated_at = clock_timestamp()
              WHERE id = $1
              RETURNING *
            `,
            [job.runId],
          );
      await client.query(
        `
          UPDATE run_jobs
          SET status = 'completed',
              lease_owner = NULL,
              lease_expires_at = NULL,
              updated_at = clock_timestamp()
          WHERE run_id = $1
        `,
        [job.runId],
      );
      await this.insertRunEvent(
        client,
        job.runId,
        job.ownerId,
        "completed",
        100,
      );

      const completed = finished.rows[0] as Row;
      const representation = this.run({
        ...completed,
        artifact_ids: [artifact.id],
      });
      await this.insertCompletionOutbox(
        client,
        job.runId,
        job.ownerId,
        completed.completed_at,
        representation,
      );
      return true;
    });
  }

  public async failJob(
    job: ClaimedJob,
    code: string,
    detail: string,
    retryable: boolean,
  ): Promise<void> {
    await this.database.transaction(async (client) => {
      const durableJob = await this.lockJob(client, job);
      const runResult = await client.query(
        "SELECT * FROM analysis_runs WHERE id = $1 FOR UPDATE",
        [job.runId],
      );
      const run = runResult.rows[0] as Row;
      if (run.cancellation_requested_at) {
        await this.cancelLocked(client, job, run);
        return;
      }

      if (retryable && durableJob.attempts < durableJob.max_attempts) {
        await client.query(
          `
            UPDATE run_jobs
            SET status = 'queued',
                available_at = clock_timestamp()
                  + ($1 || ' seconds')::interval,
                lease_owner = NULL,
                lease_expires_at = NULL,
                last_error = $2,
                updated_at = clock_timestamp()
            WHERE run_id = $3
          `,
          [retryDelaySeconds(Number(durableJob.attempts)), detail, job.runId],
        );
        await client.query(
          `
            UPDATE analysis_runs
            SET status = 'queued',
                progress = 0,
                updated_at = clock_timestamp()
            WHERE id = $1
          `,
          [job.runId],
        );
        await this.insertRunEvent(
          client,
          job.runId,
          job.ownerId,
          "queued",
          0,
        );
        return;
      }

      const failed = await client.query(
        `
          UPDATE analysis_runs
          SET status = 'failed',
              completed_at = clock_timestamp(),
              failure_code = $1,
              failure_detail = $2,
              updated_at = clock_timestamp()
          WHERE id = $3
          RETURNING *
        `,
        [code, detail, job.runId],
      );
      await client.query(
        `
          UPDATE run_jobs
          SET status = 'dead',
              lease_owner = NULL,
              lease_expires_at = NULL,
              last_error = $1,
              updated_at = clock_timestamp()
          WHERE run_id = $2
        `,
        [detail, job.runId],
      );
      const failedRun = failed.rows[0] as Row;
      await this.insertRunEvent(
        client,
        job.runId,
        job.ownerId,
        "failed",
        Number(failedRun.progress),
      );
      await this.insertFailureOutbox(
        client,
        job.runId,
        job.ownerId,
        failedRun.completed_at,
        code,
      );
    });
  }

  public async recoverExpiredJobs(): Promise<number> {
    return this.database.transaction(async (client) => {
      const result = await client.query(
        `
          SELECT
            j.*,
            r.status AS run_status,
            r.cancellation_requested_at,
            r.owner_id,
            r.progress
          FROM run_jobs AS j
          JOIN analysis_runs AS r ON r.id = j.run_id
          WHERE j.status = 'leased'
            AND j.lease_expires_at < clock_timestamp()
          ORDER BY j.updated_at
          FOR UPDATE OF j, r SKIP LOCKED
        `,
      );

      for (const row of result.rows as Row[]) {
        if (row.cancellation_requested_at) {
          const canceled = await client.query(
            `
              UPDATE analysis_runs
              SET status = 'canceled',
                  completed_at = clock_timestamp(),
                  updated_at = clock_timestamp()
              WHERE id = $1
              RETURNING *
            `,
            [row.run_id],
          );
          await client.query(
            `
              UPDATE run_jobs
              SET status = 'canceled',
                  lease_owner = NULL,
                  lease_expires_at = NULL,
                  last_error = 'lease expired after cancellation',
                  updated_at = clock_timestamp()
              WHERE run_id = $1
            `,
            [row.run_id],
          );
          await this.insertRunEvent(
            client,
            row.run_id,
            row.owner_id,
            "canceled",
            Number(canceled.rows[0]?.progress ?? row.progress),
          );
          continue;
        }

        if (row.attempts >= row.max_attempts) {
          const failed = await client.query(
            `
              UPDATE analysis_runs
              SET status = 'failed',
                  completed_at = clock_timestamp(),
                  failure_code = 'lease-exhausted',
                  failure_detail = 'worker lease expired too many times',
                  updated_at = clock_timestamp()
              WHERE id = $1
              RETURNING *
            `,
            [row.run_id],
          );
          await client.query(
            `
              UPDATE run_jobs
              SET status = 'dead',
                  lease_owner = NULL,
                  lease_expires_at = NULL,
                  last_error = 'lease exhausted',
                  updated_at = clock_timestamp()
              WHERE run_id = $1
            `,
            [row.run_id],
          );
          const failedRun = failed.rows[0] as Row;
          await this.insertRunEvent(
            client,
            row.run_id,
            row.owner_id,
            "failed",
            Number(failedRun.progress),
          );
          await this.insertFailureOutbox(
            client,
            row.run_id,
            row.owner_id,
            failedRun.completed_at,
            "lease-exhausted",
          );
          continue;
        }

        await client.query(
          `
            UPDATE run_jobs
            SET status = 'queued',
                lease_owner = NULL,
                lease_expires_at = NULL,
                available_at = clock_timestamp(),
                last_error = 'lease expired',
                updated_at = clock_timestamp()
            WHERE run_id = $1
          `,
          [row.run_id],
        );
        await client.query(
          `
            UPDATE analysis_runs
            SET status = 'queued',
                progress = 0,
                updated_at = clock_timestamp()
            WHERE id = $1 AND status = 'running'
          `,
          [row.run_id],
        );
        await this.insertRunEvent(
          client,
          row.run_id,
          row.owner_id,
          "queued",
          0,
        );
      }
      return result.rowCount ?? 0;
    });
  }

  private async cancelLocked(
    client: PoolClient,
    job: ClaimedJob,
    run: Row,
  ): Promise<void> {
    await client.query(
      `
        UPDATE analysis_runs
        SET status = 'canceled',
            completed_at = clock_timestamp(),
            updated_at = clock_timestamp()
        WHERE id = $1
      `,
      [job.runId],
    );
    await client.query(
      `
        UPDATE run_jobs
        SET status = 'canceled',
            lease_owner = NULL,
            lease_expires_at = NULL,
            updated_at = clock_timestamp()
        WHERE run_id = $1
      `,
      [job.runId],
    );
    await this.insertRunEvent(
      client,
      job.runId,
      job.ownerId,
      "canceled",
      Number(run.progress),
    );
  }

  private async insertRunEvent(
    client: PoolClient,
    runId: string,
    ownerId: string,
    status: string,
    progress: number,
  ): Promise<void> {
    await client.query(
      `
        INSERT INTO run_events(run_id, owner_id, status, progress)
        VALUES ($1, $2, $3, $4)
      `,
      [runId, ownerId, status, progress],
    );
  }

  private async insertCompletionOutbox(
    client: PoolClient,
    runId: string,
    ownerId: string,
    occurredAt: unknown,
    run: RunRepresentation,
  ): Promise<void> {
    const pending = {
      eventId: "pending",
      eventType: "analysis.completed",
      occurredAt: iso(occurredAt),
      run,
    };
    const inserted = await client.query(
      `
        INSERT INTO outbox_events(
          event_type,
          run_id,
          owner_id,
          payload
        )
        VALUES ('analysis.completed', $1, $2, $3::jsonb)
        RETURNING event_id, occurred_at
      `,
      [runId, ownerId, JSON.stringify(pending)],
    );
    const eventId = inserted.rows[0]?.event_id;
    await client.query(
      `
        UPDATE outbox_events
        SET payload = $1::jsonb
        WHERE event_id = $2
      `,
      [
        JSON.stringify({
          ...pending,
          eventId,
          occurredAt: iso(inserted.rows[0]?.occurred_at),
        }),
        eventId,
      ],
    );
  }

  private async insertFailureOutbox(
    client: PoolClient,
    runId: string,
    ownerId: string,
    occurredAt: unknown,
    failureCode: string,
  ): Promise<void> {
    const pending = {
      eventId: "pending",
      eventType: "analysis.failed",
      occurredAt: iso(occurredAt),
      runId,
      failureCode,
    };
    const inserted = await client.query(
      `
        INSERT INTO outbox_events(
          event_type,
          run_id,
          owner_id,
          payload
        )
        VALUES ('analysis.failed', $1, $2, $3::jsonb)
        RETURNING event_id, occurred_at
      `,
      [runId, ownerId, JSON.stringify(pending)],
    );
    const eventId = inserted.rows[0]?.event_id;
    await client.query(
      `
        UPDATE outbox_events
        SET payload = $1::jsonb
        WHERE event_id = $2
      `,
      [
        JSON.stringify({
          ...pending,
          eventId,
          occurredAt: iso(inserted.rows[0]?.occurred_at),
        }),
        eventId,
      ],
    );
  }

  // -----------------------------------------------------------------------
  // Transactional outbox and durable delivery
  // -----------------------------------------------------------------------
  public async expandOutbox(): Promise<number> {
    return this.database.transaction(async (client) => {
      const events = await client.query(
        `
          SELECT *
          FROM outbox_events
          WHERE expanded_at IS NULL
          ORDER BY position
          FOR UPDATE SKIP LOCKED
          LIMIT 20
        `,
      );
      for (const event of events.rows as Row[]) {
        if (event.event_type === "analysis.completed") {
          const run = await client.query(
            "SELECT callback_url FROM analysis_runs WHERE id = $1",
            [event.run_id],
          );
          const callbackUrl = run.rows[0]?.callback_url;
          if (callbackUrl) {
            await client.query(
              `
                INSERT INTO webhook_deliveries(
                  event_id,
                  delivery_kind,
                  target_url,
                  status
                )
                VALUES ($1, 'callback', $2, 'pending')
                ON CONFLICT DO NOTHING
              `,
              [event.event_id, callbackUrl],
            );
          }
        }

        const subscriptions = await client.query(
          `
            SELECT id, target_url
            FROM webhook_subscriptions
            WHERE owner_id = $1
              AND enabled
              AND $2 = ANY(event_types)
          `,
          [event.owner_id, event.event_type],
        );
        for (const subscription of subscriptions.rows as Row[]) {
          await client.query(
            `
              INSERT INTO webhook_deliveries(
                event_id,
                subscription_id,
                delivery_kind,
                target_url,
                status
              )
              VALUES ($1, $2, 'subscription', $3, 'pending')
              ON CONFLICT DO NOTHING
            `,
            [event.event_id, subscription.id, subscription.target_url],
          );
        }
        await client.query(
          `
            UPDATE outbox_events
            SET expanded_at = clock_timestamp()
            WHERE event_id = $1
          `,
          [event.event_id],
        );
      }
      return events.rowCount ?? 0;
    });
  }

  public async claimDelivery(
    workerId: string,
    leaseSeconds: number,
  ): Promise<ClaimedDelivery | null> {
    return this.database.transaction(async (client) => {
      const result = await client.query(
        `
          WITH candidate AS (
            SELECT id
            FROM webhook_deliveries
            WHERE status = 'pending'
              AND available_at <= clock_timestamp()
            ORDER BY position
            FOR UPDATE SKIP LOCKED
            LIMIT 1
          )
          UPDATE webhook_deliveries AS d
          SET status = 'leased',
              lease_owner = $1,
              lease_expires_at = clock_timestamp()
                + ($2 || ' seconds')::interval,
              lease_generation = lease_generation + 1,
              attempts = attempts + 1,
              updated_at = clock_timestamp()
          FROM candidate AS c,
               outbox_events AS o
          WHERE d.id = c.id
            AND o.event_id = d.event_id
          RETURNING
            d.id,
            d.event_id,
            d.delivery_kind,
            d.target_url,
            d.attempts,
            d.lease_generation,
            o.payload,
            CASE
              WHEN d.subscription_id IS NULL THEN $3
              ELSE (
                SELECT pgp_sym_decrypt(secret_ciphertext, $4)
                FROM webhook_subscriptions AS s
                WHERE s.id = d.subscription_id
              )
            END AS secret
        `,
        [workerId, leaseSeconds, this.callbackSecret, this.encryptionKey],
      );
      if (!(result.rowCount ?? 0)) return null;
      const row = result.rows[0] as Row;
      return {
        deliveryId: row.id,
        eventId: row.event_id,
        deliveryKind: row.delivery_kind,
        targetUrl: row.target_url,
        payload: row.payload,
        secret: row.secret,
        attempt: Number(row.attempts),
        leaseOwner: workerId,
        leaseGeneration: Number(row.lease_generation),
      };
    });
  }

  public async deliverySuccess(
    delivery: ClaimedDelivery,
    responseStatus: number,
  ): Promise<void> {
    const result = await this.database.pool.query(
      `
        UPDATE webhook_deliveries
        SET status = 'delivered',
            delivered_at = clock_timestamp(),
            response_status = $1,
            lease_owner = NULL,
            lease_expires_at = NULL,
            updated_at = clock_timestamp()
        WHERE id = $2
          AND status = 'leased'
          AND lease_owner = $3
          AND lease_generation = $4
        RETURNING id
      `,
      [
        responseStatus,
        delivery.deliveryId,
        delivery.leaseOwner,
        delivery.leaseGeneration,
      ],
    );
    if (!(result.rowCount ?? 0)) {
      throw new Error(`lease-lost:${delivery.deliveryId}`);
    }
  }

  public async deliveryFailure(
    delivery: ClaimedDelivery,
    error: string,
    retryable: boolean,
  ): Promise<void> {
    await this.database.transaction(async (client) => {
      const result = await client.query(
        `
          SELECT *
          FROM webhook_deliveries
          WHERE id = $1
            AND status = 'leased'
            AND lease_owner = $2
            AND lease_generation = $3
          FOR UPDATE
        `,
        [
          delivery.deliveryId,
          delivery.leaseOwner,
          delivery.leaseGeneration,
        ],
      );
      if (!(result.rowCount ?? 0)) {
        throw new Error(`lease-lost:${delivery.deliveryId}`);
      }
      const row = result.rows[0] as Row;
      if (retryable && row.attempts < row.max_attempts) {
        await client.query(
          `
            UPDATE webhook_deliveries
            SET status = 'pending',
                available_at = clock_timestamp()
                  + ($1 || ' seconds')::interval,
                lease_owner = NULL,
                lease_expires_at = NULL,
                last_error = $2,
                updated_at = clock_timestamp()
            WHERE id = $3
          `,
          [retryDelaySeconds(Number(row.attempts)), error, delivery.deliveryId],
        );
      } else {
        await client.query(
          `
            UPDATE webhook_deliveries
            SET status = 'dead',
                lease_owner = NULL,
                lease_expires_at = NULL,
                last_error = $1,
                updated_at = clock_timestamp()
            WHERE id = $2
          `,
          [error, delivery.deliveryId],
        );
      }
    });
  }

  public async recoverExpiredDeliveries(): Promise<number> {
    return this.database.transaction(async (client) => {
      const expired = await client.query(
        `
          SELECT *
          FROM webhook_deliveries
          WHERE status = 'leased'
            AND lease_expires_at < clock_timestamp()
          ORDER BY updated_at
          FOR UPDATE SKIP LOCKED
        `,
      );
      for (const row of expired.rows as Row[]) {
        if (row.attempts >= row.max_attempts) {
          await client.query(
            `
              UPDATE webhook_deliveries
              SET status = 'dead',
                  lease_owner = NULL,
                  lease_expires_at = NULL,
                  last_error = 'lease expired after final attempt',
                  updated_at = clock_timestamp()
              WHERE id = $1
            `,
            [row.id],
          );
        } else {
          await client.query(
            `
              UPDATE webhook_deliveries
              SET status = 'pending',
                  lease_owner = NULL,
                  lease_expires_at = NULL,
                  available_at = clock_timestamp(),
                  last_error = 'lease expired',
                  updated_at = clock_timestamp()
              WHERE id = $1
            `,
            [row.id],
          );
        }
      }
      return expired.rowCount ?? 0;
    });
  }
}
