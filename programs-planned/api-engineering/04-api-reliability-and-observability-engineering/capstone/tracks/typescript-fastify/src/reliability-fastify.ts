import type {
  FastifyInstance,
  FastifyReply,
  FastifyRequest,
} from "fastify";
import {
  InMemoryEventSink,
  LifecycleController,
  MetricRegistry,
  StructuredLogger,
  childOf,
  classifyHttpOutcome,
  evaluateHealth,
  formatTraceparent,
  newRoot,
  parseTraceparent,
  type TraceContext,
} from "./reliability/index.js";

export interface ReliabilityRuntime {
  readonly lifecycle: LifecycleController;
  readonly registry: MetricRegistry;
  readonly events: InMemoryEventSink;
  beginDrain(reason?: string): void;
  recordRunStart(withinObjective: boolean): void;
  setOldestQueueAge(seconds: number): void;
}

interface RequestState {
  readonly startedMs: number;
  readonly context: TraceContext;
}

export function installReliability(
  app: FastifyInstance,
  input: {
    readonly lifecycle: LifecycleController;
    readonly readinessCheck: () => Promise<void>;
    readonly serviceName: string;
    readonly serviceVersion: string;
    readonly environment: string;
  },
): ReliabilityRuntime {
  const registry = new MetricRegistry();
  const events = new InMemoryEventSink(10_000);
  const logger = new StructuredLogger({
    nowMs: () => Date.now(),
    sink: events,
    serviceName: input.serviceName,
    serviceVersion: input.serviceVersion,
    deploymentEnvironment: input.environment,
    schemaVersion: "1.0",
  });
  const requests = registry.counter({
    name: "analysis_http_server_requests_total",
    description: "Completed HTTP requests classified for the availability SLI",
    unit: "{request}",
    labels: ["operation", "eligibility", "outcome", "status_class"],
    maxSeries: 800,
  });
  const duration = registry.histogram({
    name: "analysis_http_server_duration_seconds",
    description: "HTTP server request duration by stable operation identifier",
    unit: "s",
    labels: ["operation"],
    maxSeries: 64,
  }, [0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]);
  const active = registry.gauge({
    name: "analysis_http_server_active_requests",
    description: "Requests currently executing inside the application",
    unit: "{request}",
  });
  const dropped = registry.counter({
    name: "analysis_telemetry_dropped_total",
    description: "Structured operational events dropped by the bounded local sink",
    unit: "{event}",
  });
  const runStarts = registry.counter({
    name: "analysis_run_start_total",
    description: "Accepted runs classified against the run-start objective",
    unit: "{run}",
    labels: ["outcome"],
    maxSeries: 2,
  });
  const oldestQueueAge = registry.gauge({
    name: "analysis_worker_oldest_queued_age_seconds",
    description: "Age in seconds of the oldest runnable queued job",
    unit: "s",
  });
  const states = new WeakMap<object, RequestState>();
  let activeCount = 0;
  let reportedDrops = 0;

  const accountForDrops = (): void => {
    const delta = events.dropped - reportedDrops;
    if (delta > 0) {
      dropped.add(delta);
      reportedDrops = events.dropped;
    }
  };

  app.addHook("onRequest", async (request) => {
    let parent: TraceContext;
    const value = request.headers.traceparent;
    try {
      parent = typeof value === "string" ? parseTraceparent(value) : newRoot(false);
    } catch {
      parent = newRoot(false);
      logger.emit("http.trace_context.rejected", {
        severity: "WARN",
        attributes: { reason: "invalid-traceparent" },
      });
    }
    const context = childOf(parent);
    states.set(request, { startedMs: performance.now(), context });
    activeCount += 1;
    active.set(activeCount);
  });

  app.addHook("onSend", async (request, reply, payload) => {
    const state = states.get(request);
    if (state !== undefined) reply.header("traceparent", formatTraceparent(state.context));
    return payload;
  });

  app.addHook("onResponse", async (request, reply) => {
    const state = states.get(request);
    const elapsed = state === undefined
      ? 0
      : (performance.now() - state.startedMs) / 1_000;
    const operation = operationId(request);
    const { eligibility, outcome } = classifyHttpOutcome(operation, reply.statusCode);
    requests.add(1, {
      operation,
      eligibility,
      outcome,
      status_class: `${Math.floor(reply.statusCode / 100)}xx`,
    });
    duration.observe(elapsed, { operation });
    logger.emit("http.server.request.completed", {
      severity: reply.statusCode >= 500 ? "ERROR" : "INFO",
      ...(state === undefined ? {} : { context: state.context }),
      attributes: {
        "http.request.method": request.method,
        "http.route.operation_id": operation,
        "http.response.status_code": reply.statusCode,
        "sli.eligibility": eligibility,
        "sli.outcome": outcome,
        duration_ms: Math.round(elapsed * 1_000_000) / 1_000,
      },
    });
    states.delete(request);
    activeCount = Math.max(0, activeCount - 1);
    active.set(activeCount);
    accountForDrops();
  });

  app.get("/internal/health/live", { schema: { hide: true } }, async (_request, reply) => {
    const snapshot = evaluateHealth({
      phase: input.lifecycle.phase,
      startupComplete: input.lifecycle.phase !== "starting",
      eventLoopProgressing: true,
      components: [],
    });
    reply.code(snapshot.live ? 200 : 503);
    return snapshot;
  });

  app.get("/internal/health/ready", { schema: { hide: true } }, async (_request, reply) => {
    let available = true;
    let detail = "available";
    try {
      await input.readinessCheck();
    } catch (error) {
      available = false;
      detail = error instanceof Error ? error.name : "UnknownError";
    }
    const snapshot = evaluateHealth({
      phase: input.lifecycle.phase,
      startupComplete: input.lifecycle.phase !== "starting",
      eventLoopProgressing: true,
      components: [{ name: "postgresql", requiredForReadiness: true, available, detail }],
    });
    reply.code(snapshot.ready ? 200 : 503);
    return snapshot;
  });

  app.get("/internal/metrics", { schema: { hide: true } }, async (_request, reply) => {
    accountForDrops();
    reply.type("application/openmetrics-text; version=1.0.0; charset=utf-8");
    return registry.renderPrometheus();
  });

  return {
    lifecycle: input.lifecycle,
    registry,
    events,
    beginDrain(reason = "shutdown-requested"): void {
      if (["starting", "accepting"].includes(input.lifecycle.phase)) {
        input.lifecycle.transition("draining", { reason, timestampMs: Date.now() });
      }
    },
    recordRunStart(withinObjective: boolean): void {
      runStarts.add(1, { outcome: withinObjective ? "good" : "bad" });
    },
    setOldestQueueAge(seconds: number): void {
      oldestQueueAge.set(Math.max(0, seconds));
    },
  };
}

function operationId(request: FastifyRequest): string {
  const routed = request as FastifyRequest & {
    readonly routeOptions?: {
      readonly schema?: { readonly operationId?: unknown };
      readonly url?: string;
    };
  };
  const schema = routed.routeOptions?.schema;
  return typeof schema?.operationId === "string" && schema.operationId !== ""
    ? schema.operationId
    : routed.routeOptions?.url ?? "unmatched";
}
