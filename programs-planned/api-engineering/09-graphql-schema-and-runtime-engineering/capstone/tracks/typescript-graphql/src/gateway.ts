import { analyze, defaultCostPolicy, type CostPolicy } from "./cost.js";
import {
  CursorCodec,
  audienceHash,
  normalizedFilterHash,
  type CursorState,
} from "./cursor.js";
import { decodeGlobalId, encodeGlobalId } from "./identity.js";
import { BatchLoader } from "./loader.js";
import {
  AuthorizationError,
  ConflictError,
  DownstreamUnavailable,
  PreconditionFailed,
  ValidationError,
  type ExecutionResult,
  type GraphError,
  type RequestContext,
} from "./model.js";
import { parseDocument } from "./operation.js";
import { PersistedOperationRegistry } from "./persisted.js";
import { requireField } from "./policy.js";
import {
  AnalysisControlClient,
  ArtifactServiceClient,
  NotificationServiceClient,
  type AnalysisSearchItem,
  type Artifact,
  type Project,
  type Run,
} from "./services.js";
import { ResumableSubscription } from "./subscription.js";

type SortKey = readonly [string, string];
type ConnectionValue = Record<string, unknown>;

function compareKey(left: SortKey, right: SortKey): number {
  return left[0].localeCompare(right[0]) || left[1].localeCompare(right[1]);
}

export class AnalysisGraphGateway {
  constructor(
    readonly registry: PersistedOperationRegistry,
    readonly analysis = new AnalysisControlClient(),
    readonly artifacts = new ArtifactServiceClient(),
    readonly notifications = new NotificationServiceClient(),
    readonly cursorCodec = new CursorCodec(
      Buffer.from("course-cursor-key-0123456789abcdef"),
    ),
    readonly costPolicy: CostPolicy = defaultCostPolicy,
    readonly cursorTtlSeconds = 3_600,
  ) {}

  execute(
    hash: string,
    variables: Record<string, unknown>,
    context: RequestContext,
  ): ExecutionResult {
    try {
      const operation = this.registry.get(hash);
      const report = analyze(
        parseDocument(operation.document),
        operation.name,
        variables,
        this.costPolicy,
      );
      const result = this.dispatch(operation.name, variables, context);
      return {
        ...result,
        extensions: {
          cost: report.estimatedCost,
          serviceFanout: report.serviceFanout,
          ...result.extensions,
        },
      };
    } catch (error) {
      if (error instanceof AuthorizationError) {
        return {
          data: null,
          errors: [{ message: "Not authorized", code: "FORBIDDEN" }],
        };
      }
      if (error instanceof ValidationError) {
        return {
          data: null,
          errors: [
            { message: error.message, code: "GRAPHQL_VALIDATION_FAILED" },
          ],
        };
      }
      if (error instanceof DownstreamUnavailable) {
        return {
          data: null,
          errors: [
            {
              message: "A required source is temporarily unavailable",
              code: "DOWNSTREAM_UNAVAILABLE",
              service: error.service,
            },
          ],
        };
      }
      throw error;
    }
  }

  private dispatch(
    name: string,
    variables: Record<string, unknown>,
    context: RequestContext,
  ): ExecutionResult {
    switch (name) {
      case "Viewer":
        return this.viewer(context);
      case "GetProjectOverview":
        return this.getProjectOverview(variables, context);
      case "GetRun":
        return this.getRun(variables, context);
      case "ListRuns":
        return this.listRuns(variables, context);
      case "SearchPlatform":
        return this.searchPlatform(variables, context);
      case "CreateProject":
        return this.createProject(variables, context);
      case "StartAnalysis":
        return this.startAnalysis(variables, context);
      case "CancelAnalysis":
        return this.cancelAnalysis(variables, context);
      case "RunUpdates":
        return this.runUpdates(variables, context);
      case "NodeLookup":
        return this.nodeLookup(variables, context);
      default:
        throw new ValidationError("operation has no executor");
    }
  }

  private projectNode(project: Project): ConnectionValue {
    return {
      id: encodeGlobalId("Project", project.id),
      name: project.name,
      version: project.version,
    };
  }

  private runNode(run: Run): ConnectionValue {
    return {
      id: encodeGlobalId("AnalysisRun", run.id),
      projectId: encodeGlobalId("Project", run.projectId),
      datasetId: run.datasetId,
      status: run.status,
      version: run.version,
      createdAt: run.createdAt,
      resultSummary: run.resultSummary,
    };
  }

  private artifactNode(artifact: Artifact): ConnectionValue {
    return {
      id: encodeGlobalId("Artifact", artifact.id),
      runId: encodeGlobalId("AnalysisRun", artifact.runId),
      mediaType: artifact.mediaType,
      size: artifact.size,
      sha256: artifact.sha256,
      downloadUrl: artifact.downloadUrl,
    };
  }

  private connection<T>(options: {
    values: readonly T[];
    keyOf: (value: T) => SortKey;
    nodeOf: (value: T) => ConnectionValue;
    scope: string;
    filter: Record<string, unknown>;
    first: number;
    after?: string;
    context: RequestContext;
  }): ConnectionValue {
    if (
      !Number.isSafeInteger(options.first) ||
      options.first < 1 ||
      options.first > this.costPolicy.maxPageSize
    ) {
      throw new ValidationError(
        `first outside 1..${this.costPolicy.maxPageSize}`,
      );
    }

    const ordered = [...options.values].sort((left, right) =>
      compareKey(options.keyOf(right), options.keyOf(left)),
    );
    if (!ordered.length) {
      return {
        edges: [],
        pageInfo: { hasNextPage: false, endCursor: null },
      };
    }

    const filterHash = normalizedFilterHash(options.filter);
    const callerHash = audienceHash(options.context.principal);
    let highWater = options.keyOf(ordered[0]!);
    let afterKey: SortKey | undefined;

    if (options.after) {
      const state = this.cursorCodec.decode(options.after, {
        tenantId: options.context.principal.tenantId,
        audienceHash: callerHash,
        scope: options.scope,
        filterHash,
        nowEpoch: options.context.nowEpoch,
      });
      highWater = [state.highWaterPrimary, state.highWaterTiebreaker];
      afterKey = [state.afterPrimary, state.afterTiebreaker];
    }

    const eligible = ordered.filter((value) => {
      const key = options.keyOf(value);
      return (
        compareKey(key, highWater) <= 0 &&
        (afterKey === undefined || compareKey(key, afterKey) < 0)
      );
    });
    const selected = eligible.slice(0, options.first + 1);
    const page = selected.slice(0, options.first);
    const hasNextPage = selected.length > options.first;

    const edges = page.map((value) => {
      const key = options.keyOf(value);
      const state: CursorState = {
        tenantId: options.context.principal.tenantId,
        audienceHash: callerHash,
        scope: options.scope,
        filterHash,
        afterPrimary: key[0],
        afterTiebreaker: key[1],
        highWaterPrimary: highWater[0],
        highWaterTiebreaker: highWater[1],
        expiresAt: options.context.nowEpoch + this.cursorTtlSeconds,
        version: 1,
      };
      return { cursor: this.cursorCodec.encode(state), node: options.nodeOf(value) };
    });

    return {
      edges,
      pageInfo: {
        hasNextPage,
        endCursor: edges.at(-1)?.cursor ?? null,
      },
    };
  }

  private viewer(context: RequestContext): ExecutionResult {
    const principal = context.principal;
    return {
      data: {
        viewer: {
          subject: principal.subject,
          tenantId: principal.tenantId,
          permissions: [...principal.permissions].sort(),
        },
      },
    };
  }

  private getProjectOverview(
    variables: Record<string, unknown>,
    context: RequestContext,
  ): ExecutionResult {
    const principal = context.principal;
    requireField(principal, "Query.project");
    const [typeName, projectId] = decodeGlobalId(String(variables.projectId));
    if (typeName !== "Project") {
      throw new ValidationError("projectId has the wrong global identifier type");
    }
    const project = this.analysis.getProject(principal, projectId);
    if (!project) {
      return { data: { project: null } };
    }

    const runs = this.analysis.listRuns(principal, projectId);
    const connection = this.connection({
      values: runs,
      keyOf: (run) => [run.createdAt, run.id],
      nodeOf: (run) => this.runNode(run),
      scope: "Project.analysisRuns",
      filter: { projectId },
      first: Number(variables.first ?? 20),
      after:
        typeof variables.after === "string" ? variables.after : undefined,
      context,
    });

    const edges = connection.edges as Array<{
      cursor: string;
      node: Record<string, unknown>;
    }>;
    const runById = new Map(runs.map((run) => [run.id, run]));
    const artifactLoader = new BatchLoader<string, readonly Artifact[]>((keys) =>
      this.artifacts.batchByRun(principal, keys),
    );
    const deliveryLoader = new BatchLoader<string, Record<string, unknown>>(
      (keys) => this.notifications.batchByRun(principal, keys),
    );
    const artifactAllowed = principal.permissions.has("ARTIFACT_READ");
    const deliveryAllowed = principal.permissions.has("DELIVERY_READ");
    const artifactTokens = new Map<string, ReturnType<typeof artifactLoader.load>>();
    const deliveryTokens = new Map<string, ReturnType<typeof deliveryLoader.load>>();
    const errors: GraphError[] = [];

    for (const edge of edges) {
      const [, runId] = decodeGlobalId(String(edge.node.id));
      if (artifactAllowed) artifactTokens.set(runId, artifactLoader.load(runId));
      if (deliveryAllowed) deliveryTokens.set(runId, deliveryLoader.load(runId));
    }

    let artifactFailed = false;
    let deliveryFailed = false;
    if (artifactAllowed) {
      try {
        artifactLoader.dispatch();
      } catch (error) {
        if (!(error instanceof DownstreamUnavailable)) throw error;
        artifactFailed = true;
      }
    }
    if (deliveryAllowed) {
      try {
        deliveryLoader.dispatch();
      } catch (error) {
        if (!(error instanceof DownstreamUnavailable)) throw error;
        deliveryFailed = true;
      }
    }

    edges.forEach((edge, index) => {
      const [, runId] = decodeGlobalId(String(edge.node.id));
      const run = runById.get(runId)!;
      const artifactPath = [
        "project",
        "analysisRuns",
        "edges",
        index,
        "node",
        "artifacts",
      ] as const;
      const deliveryPath = [
        "project",
        "analysisRuns",
        "edges",
        index,
        "node",
        "deliverySummary",
      ] as const;

      if (!artifactAllowed) {
        edge.node.artifacts = null;
        errors.push({ message: "Not authorized", path: artifactPath, code: "FORBIDDEN" });
      } else if (artifactFailed) {
        edge.node.artifacts = null;
        errors.push({
          message: "Artifact data is temporarily unavailable",
          path: artifactPath,
          code: "DOWNSTREAM_UNAVAILABLE",
          service: "artifact-service",
        });
      } else {
        edge.node.artifacts = (artifactTokens.get(run.id)?.get() ?? []).map(
          (artifact) => this.artifactNode(artifact),
        );
      }

      if (!deliveryAllowed) {
        edge.node.deliverySummary = null;
        errors.push({ message: "Not authorized", path: deliveryPath, code: "FORBIDDEN" });
      } else if (deliveryFailed) {
        edge.node.deliverySummary = null;
        errors.push({
          message: "Delivery data is temporarily unavailable",
          path: deliveryPath,
          code: "DOWNSTREAM_UNAVAILABLE",
          service: "notification-service",
        });
      } else {
        edge.node.deliverySummary = deliveryTokens.get(run.id)?.get() ?? null;
      }
    });

    return {
      data: {
        project: { ...this.projectNode(project), analysisRuns: connection },
      },
      errors,
      extensions: {
        batchCalls: {
          artifact: artifactLoader.dispatches,
          delivery: deliveryLoader.dispatches,
        },
      },
    };
  }

  private getRun(
    variables: Record<string, unknown>,
    context: RequestContext,
  ): ExecutionResult {
    const principal = context.principal;
    requireField(principal, "Query.analysisRun");
    const [typeName, runId] = decodeGlobalId(String(variables.runId));
    if (typeName !== "AnalysisRun") {
      throw new ValidationError("runId has the wrong global identifier type");
    }
    const run = this.analysis.getRun(principal, runId);
    if (!run) return { data: { analysisRun: null } };

    const node = this.runNode(run);
    const errors: GraphError[] = [];
    if (!principal.permissions.has("ARTIFACT_READ")) {
      node.artifacts = null;
      errors.push({
        message: "Not authorized",
        path: ["analysisRun", "artifacts"],
        code: "FORBIDDEN",
      });
    } else {
      try {
        node.artifacts = (
          this.artifacts.batchByRun(principal, [runId]).get(runId) ?? []
        ).map((artifact) => this.artifactNode(artifact));
      } catch (error) {
        if (!(error instanceof DownstreamUnavailable)) throw error;
        node.artifacts = null;
        errors.push({
          message: "Artifact data is temporarily unavailable",
          path: ["analysisRun", "artifacts"],
          code: "DOWNSTREAM_UNAVAILABLE",
          service: error.service,
        });
      }
    }

    if (!principal.permissions.has("DELIVERY_READ")) {
      node.deliverySummary = null;
      errors.push({
        message: "Not authorized",
        path: ["analysisRun", "deliverySummary"],
        code: "FORBIDDEN",
      });
    } else {
      try {
        node.deliverySummary =
          this.notifications.batchByRun(principal, [runId]).get(runId) ?? null;
      } catch (error) {
        if (!(error instanceof DownstreamUnavailable)) throw error;
        node.deliverySummary = null;
        errors.push({
          message: "Delivery data is temporarily unavailable",
          path: ["analysisRun", "deliverySummary"],
          code: "DOWNSTREAM_UNAVAILABLE",
          service: error.service,
        });
      }
    }
    return { data: { analysisRun: node }, errors };
  }

  private listRuns(
    variables: Record<string, unknown>,
    context: RequestContext,
  ): ExecutionResult {
    requireField(context.principal, "Query.analysisRun");
    const filter = { ...((variables.filter as Record<string, unknown>) ?? {}) };
    let projectId: string | undefined;
    if (typeof filter.projectId === "string") {
      const [typeName, localId] = decodeGlobalId(filter.projectId);
      if (typeName !== "Project") {
        throw new ValidationError("filter.projectId has the wrong type");
      }
      projectId = localId;
      filter.projectId = localId;
    }
    const values = this.analysis.listRuns(
      context.principal,
      projectId,
      typeof filter.status === "string" ? filter.status : undefined,
    );
    return {
      data: {
        analysisRuns: this.connection({
          values,
          keyOf: (run) => [run.createdAt, run.id],
          nodeOf: (run) => this.runNode(run),
          scope: "Query.analysisRuns",
          filter,
          first: Number(variables.first ?? 20),
          after:
            typeof variables.after === "string" ? variables.after : undefined,
          context,
        }),
      },
    };
  }

  private searchPlatform(
    variables: Record<string, unknown>,
    context: RequestContext,
  ): ExecutionResult {
    const text = String(variables.text).trim();
    if (!text || text.length > 200) {
      throw new ValidationError("search text must contain 1..200 characters");
    }
    const items: Array<
      | AnalysisSearchItem
      | { type: "Artifact"; value: Artifact }
    > = [...this.analysis.search(context.principal, text)];
    if (context.principal.permissions.has("ARTIFACT_READ")) {
      items.push(
        ...this.artifacts
          .search(context.principal, text)
          .map((value) => ({ type: "Artifact" as const, value })),
      );
    }

    const keyOf = (item: (typeof items)[number]): SortKey => {
      const value = item.value;
      const haystack = Object.values(value).join(" ").toLocaleLowerCase();
      const score = haystack.startsWith(text.toLocaleLowerCase()) ? 3 : 2;
      return [String(score).padStart(3, "0"), `${item.type}:${value.id}`];
    };
    const nodeOf = (item: (typeof items)[number]): ConnectionValue => {
      if (item.type === "Project") {
        return { __typename: "Project", ...this.projectNode(item.value) };
      }
      if (item.type === "AnalysisRun") {
        return { __typename: "AnalysisRun", ...this.runNode(item.value) };
      }
      return { __typename: "Artifact", ...this.artifactNode(item.value) };
    };
    return {
      data: {
        search: this.connection({
          values: items,
          keyOf,
          nodeOf,
          scope: "Query.search",
          filter: { text: text.toLocaleLowerCase() },
          first: Number(variables.first ?? 20),
          after:
            typeof variables.after === "string" ? variables.after : undefined,
          context,
        }),
      },
    };
  }

  private createProject(
    variables: Record<string, unknown>,
    context: RequestContext,
  ): ExecutionResult {
    requireField(context.principal, "Mutation.createProject");
    const input = variables.input as Record<string, unknown>;
    try {
      const outcome = this.analysis.createProject(
        context.principal,
        String(input.idempotencyKey),
        String(input.name),
      );
      return {
        data: {
          createProject: {
            clientMutationId: input.clientMutationId ?? null,
            project: this.projectNode(outcome.project),
            replayed: outcome.replayed,
          },
        },
      };
    } catch (error) {
      if (!(error instanceof ConflictError)) throw error;
      return {
        data: {
          createProject: {
            clientMutationId: input.clientMutationId ?? null,
            code: "CONFLICT",
            message: "Idempotency key is bound to another input",
            field: "idempotencyKey",
          },
        },
      };
    }
  }

  private startAnalysis(
    variables: Record<string, unknown>,
    context: RequestContext,
  ): ExecutionResult {
    requireField(context.principal, "Mutation.startAnalysis");
    const input = variables.input as Record<string, unknown>;
    const [typeName, projectId] = decodeGlobalId(String(input.projectId));
    if (typeName !== "Project") {
      throw new ValidationError("projectId has the wrong global identifier type");
    }
    try {
      const outcome = this.analysis.startAnalysis(
        context.principal,
        String(input.idempotencyKey),
        projectId,
        String(input.datasetId),
        String(input.algorithm),
      );
      return {
        data: {
          startAnalysis: {
            clientMutationId: input.clientMutationId ?? null,
            replayed: outcome.replayed,
            run: this.runNode(outcome.run),
          },
        },
      };
    } catch (error) {
      if (error instanceof ConflictError) {
        return {
          data: {
            startAnalysis: {
              clientMutationId: input.clientMutationId ?? null,
              code: "CONFLICT",
              message: "Idempotency key is bound to another input",
              field: "idempotencyKey",
            },
          },
        };
      }
      if (error instanceof Error && error.message === "not-found") {
        return {
          data: {
            startAnalysis: {
              clientMutationId: input.clientMutationId ?? null,
              code: "NOT_FOUND",
              message: "Project was not found",
              field: "projectId",
            },
          },
        };
      }
      throw error;
    }
  }

  private cancelAnalysis(
    variables: Record<string, unknown>,
    context: RequestContext,
  ): ExecutionResult {
    requireField(context.principal, "Mutation.cancelAnalysis");
    const input = variables.input as Record<string, unknown>;
    const [typeName, runId] = decodeGlobalId(String(input.runId));
    if (typeName !== "AnalysisRun") {
      throw new ValidationError("runId has the wrong global identifier type");
    }
    try {
      const run = this.analysis.cancel(
        context.principal,
        runId,
        String(input.expectedVersion),
      );
      return {
        data: {
          cancelAnalysis: {
            clientMutationId: input.clientMutationId ?? null,
            run: this.runNode(run),
          },
        },
      };
    } catch (error) {
      if (error instanceof PreconditionFailed) {
        return {
          data: {
            cancelAnalysis: {
              clientMutationId: input.clientMutationId ?? null,
              code: "PRECONDITION_FAILED",
              message: "Run version changed",
              field: "expectedVersion",
            },
          },
        };
      }
      if (error instanceof ConflictError) {
        return {
          data: {
            cancelAnalysis: {
              clientMutationId: input.clientMutationId ?? null,
              code: "CONFLICT",
              message: "Run is already terminal",
              field: "runId",
            },
          },
        };
      }
      if (error instanceof Error && error.message === "not-found") {
        return {
          data: {
            cancelAnalysis: {
              clientMutationId: input.clientMutationId ?? null,
              code: "NOT_FOUND",
              message: "Run was not found",
              field: "runId",
            },
          },
        };
      }
      throw error;
    }
  }

  private runUpdates(
    variables: Record<string, unknown>,
    context: RequestContext,
  ): ExecutionResult {
    requireField(context.principal, "Subscription.analysisRunUpdated");
    const [typeName, runId] = decodeGlobalId(String(variables.runId));
    if (typeName !== "AnalysisRun") {
      throw new ValidationError("runId has the wrong global identifier type");
    }
    const after = Number(variables.afterSequence ?? 0);
    if (!Number.isSafeInteger(after) || after < 0) {
      throw new ValidationError("afterSequence is invalid");
    }
    const source = this.analysis
      .updates(context.principal, runId, after)
      .map((event) => ({ sequence: Number(event.sequence), payload: event }));
    const delivered = new ResumableSubscription().resume(source, after);
    return {
      data: {
        analysisRunUpdated: delivered.map((event) => ({
          sequence: String(event.sequence),
          occurredAt: "2026-08-08T12:00:00Z",
          run: this.runNode(event.payload.run as Run),
        })),
      },
    };
  }

  private nodeLookup(
    variables: Record<string, unknown>,
    context: RequestContext,
  ): ExecutionResult {
    const input = variables.by as Record<string, unknown>;
    const present = Object.entries(input).filter(([, value]) => value != null);
    if (present.length !== 1) {
      throw new ValidationError("NodeLookup requires exactly one non-null field");
    }

    let typeName: string;
    let localId: string;
    if (typeof input.id === "string") {
      [typeName, localId] = decodeGlobalId(input.id);
    } else {
      const externalId = String(input.externalId);
      const analysis = this.analysis.resolveExternalId(
        context.principal,
        externalId,
      );
      if (analysis) {
        typeName = analysis.type;
        localId = analysis.value.id;
      } else {
        const artifact = this.artifacts.resolveExternalId(
          context.principal,
          externalId,
        );
        if (!artifact) return { data: { node: null } };
        typeName = "Artifact";
        localId = artifact.id;
      }
    }

    let exists = false;
    if (typeName === "Project") {
      requireField(context.principal, "Query.project");
      exists = this.analysis.getProject(context.principal, localId) !== undefined;
    } else if (typeName === "AnalysisRun") {
      requireField(context.principal, "Query.analysisRun");
      exists = this.analysis.getRun(context.principal, localId) !== undefined;
    } else if (typeName === "Artifact") {
      requireField(context.principal, "Query.artifact");
      exists = this.artifacts.get(context.principal, localId) !== undefined;
    } else {
      throw new ValidationError("unsupported node type");
    }

    return {
      data: {
        node: exists
          ? { __typename: typeName, id: encodeGlobalId(typeName, localId) }
          : null,
      },
    };
  }
}
