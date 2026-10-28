import { createHash } from "node:crypto";
import { createReadStream } from "node:fs";
import { setTimeout as sleep } from "node:timers/promises";
import { pathToFileURL } from "node:url";

import { FileSystemArtifactStore } from "./artifacts.js";
import { settingsFromEnvironment, type Settings } from "./config.js";
import { Database } from "./db.js";
import { canonicalJson } from "./domain.js";
import { PostgresRepository } from "./repository.js";
import {
  RemoteFixtureError,
  resolveRemoteFixture,
} from "./remoteFixtures.js";
import type { ClaimedJob } from "./types.js";
import {
  canonicalWebhookBody,
  OutboundWebhookTransport,
  webhookSignature,
} from "./webhooks.js";

const READ_CHUNK_SIZE = 64 * 1024;

class PermanentJobFailure extends Error {
  public constructor(message: string) {
    super(message);
    this.name = "PermanentJobFailure";
  }
}

export class Worker {
  private stopping = false;

  public constructor(
    private readonly repository: PostgresRepository,
    private readonly store: FileSystemArtifactStore,
    private readonly transport: OutboundWebhookTransport,
    private readonly settings: Settings,
  ) {}

  public stop(): void {
    this.stopping = true;
  }

  public async processOneJob(): Promise<boolean> {
    const job = await this.repository.claimJob(
      this.settings.workerId,
      this.settings.workerLeaseSeconds,
    );
    if (!job) return false;

    try {
      await this.repository.markJobRunning(job);
      const result = await this.analyze(job);
      await this.repository.renewJobLease(
        job,
        this.settings.workerLeaseSeconds,
      );

      // Python and TypeScript publish the exact same canonical bytes.
      const staged = await this.store.stageBytes(
        Buffer.from(canonicalJson(result), "utf8"),
        "application/json",
      );
      const storageKey =
        `artifacts/${staged.checksumSha256.slice(0, 2)}/` +
        staged.checksumSha256;
      await this.store.publish(staged, storageKey);
      await this.repository.completeJob(
        job,
        staged,
        storageKey,
        `${job.algorithm}.json`,
        { algorithm: job.algorithm, artifactCount: 1 },
      );
    } catch (error) {
      if (isLeaseLost(error)) {
        console.warn(
          JSON.stringify({
            event: "stale-worker-result-rejected",
            runId: job.runId,
            generation: job.leaseGeneration,
          }),
        );
      } else {
        const retryable = !(error instanceof PermanentJobFailure);
        console.error(
          JSON.stringify({
            event: retryable ? "job-retryable-failure" : "job-dead-letter",
            runId: job.runId,
            attempt: job.attempt,
            error: String(error),
          }),
        );
        try {
          await this.repository.failJob(
            job,
            "worker-error",
            error instanceof Error ? error.message : String(error),
            retryable,
          );
        } catch (nested) {
          if (!isLeaseLost(nested)) throw nested;
        }
      }
    }
    return true;
  }

  public async processOneDelivery(): Promise<boolean> {
    await this.repository.expandOutbox();
    const delivery = await this.repository.claimDelivery(
      this.settings.workerId,
      this.settings.workerLeaseSeconds,
    );
    if (!delivery) return false;

    const body = canonicalWebhookBody(delivery.payload);
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const headers = {
      "Content-Type": "application/json",
      "X-Event-Id": delivery.eventId,
      "X-Webhook-Timestamp": timestamp,
      "X-Webhook-Signature": webhookSignature(
        delivery.secret,
        timestamp,
        body,
      ),
    };

    try {
      const status = await this.transport.post(
        delivery.targetUrl,
        body,
        headers,
        3_000,
      );
      if (status >= 200 && status < 300) {
        await this.repository.deliverySuccess(delivery, status);
      } else {
        const retryable =
          status >= 500 || [408, 425, 429].includes(status);
        await this.repository.deliveryFailure(
          delivery,
          `receiver returned ${status}`,
          retryable,
        );
      }
    } catch (error) {
      if (isLeaseLost(error)) {
        console.warn(
          JSON.stringify({
            event: "delivery-lease-lost",
            eventId: delivery.eventId,
          }),
        );
      } else {
        try {
          await this.repository.deliveryFailure(
            delivery,
            error instanceof Error ? error.message : String(error),
            true,
          );
        } catch (nested) {
          if (!isLeaseLost(nested)) throw nested;
        }
      }
    }
    return true;
  }

  public async run(): Promise<void> {
    while (!this.stopping) {
      await this.repository.recoverExpiredJobs();
      await this.repository.recoverExpiredDeliveries();

      // Evaluate both paths. A permanently busy job queue must not starve the
      // webhook dispatcher, and a delivery backlog must not starve analysis.
      const processedJob = await this.processOneJob();
      const processedDelivery = await this.processOneDelivery();
      if (!processedJob && !processedDelivery) await sleep(250);
    }
  }

  private async analyze(job: ClaimedJob): Promise<Record<string, unknown>> {
    const path = await this.sourcePath(job);
    const hash = createHash("sha256");
    let bytes = 0;
    let lines = 0;
    let lastByte = -1;
    let chunks = 0;

    for await (const raw of createReadStream(path, {
      highWaterMark: READ_CHUNK_SIZE,
    })) {
      const chunk = raw as Buffer;
      hash.update(chunk);
      bytes += chunk.length;
      for (const octet of chunk) {
        if (octet === 10) lines += 1;
      }
      lastByte = chunk.at(-1) ?? lastByte;
      chunks += 1;
      if (chunks % 8 === 0) {
        await this.repository.renewJobLease(
          job,
          this.settings.workerLeaseSeconds,
        );
      }
    }
    if (bytes > 0 && lastByte !== 10) lines += 1;

    const actualChecksum = hash.digest("hex");
    const expectedChecksum =
      job.expectedChecksum ??
      (job.source.kind === "remote-object"
        ? job.source.checksumSha256
        : undefined);
    if (expectedChecksum && expectedChecksum !== actualChecksum) {
      throw new PermanentJobFailure(
        "dataset checksum does not match the durable contract",
      );
    }

    const common = {
      algorithm: job.algorithm,
      bytes,
      sha256: actualChecksum,
    };
    if (job.algorithm === "checksum") return common;
    if (job.algorithm === "line-count") return { ...common, lines };
    return { ...common, lines, nonEmpty: bytes > 0 };
  }

  private async sourcePath(job: ClaimedJob): Promise<string> {
    if (job.sourceKind === "local-file") {
      if (!job.contentPath) {
        throw new PermanentJobFailure(
          "ready local dataset has no content path",
        );
      }
      return this.store.pathFor(job.contentPath, job.expectedChecksum ?? undefined);
    }

    if (job.source.kind !== "remote-object") {
      throw new PermanentJobFailure(
        "remote-object job carries a local-file source",
      );
    }
    return resolveRemoteFixture(
      this.settings.remoteFixtureRoot,
      job.source.uri,
    );
  }
}

function isLeaseLost(error: unknown): boolean {
  return error instanceof Error && error.message.startsWith("lease-lost:");
}

async function main(): Promise<void> {
  const settings = settingsFromEnvironment();
  const database = new Database(settings.databaseUrl);
  const repository = new PostgresRepository(
    database,
    settings.webhookEncryptionKey,
    settings.callbackSigningSecret,
    settings.serviceRelease,
  );
  const worker = new Worker(
    repository,
    new FileSystemArtifactStore(settings.artifactRoot),
    new OutboundWebhookTransport(settings.webhookTransportBase),
    settings,
  );

  const stop = (): void => worker.stop();
  process.on("SIGINT", stop);
  process.on("SIGTERM", stop);
  try {
    await worker.run();
  } finally {
    await repository.close();
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
}
