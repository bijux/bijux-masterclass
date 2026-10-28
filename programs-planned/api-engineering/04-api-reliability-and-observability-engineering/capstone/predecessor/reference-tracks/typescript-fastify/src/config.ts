import { mkdirSync } from "node:fs";
import { resolve } from "node:path";

export type ServiceRelease = "1.0" | "1.1";

export type Settings = Readonly<{
  databaseUrl: string;
  artifactRoot: string;
  remoteFixtureRoot: string;
  webhookTransportBase: string;
  webhookEncryptionKey: string;
  callbackSigningSecret: string;
  workerId: string;
  workerLeaseSeconds: number;
  uploadLimitBytes: number;
  serviceRelease: ServiceRelease;
  publicApiVersion: "1.1.0" | "1.2.0";
  environment: string;
}>;

const COURSE_ENCRYPTION_KEY = "course-training-encryption-key";
const COURSE_CALLBACK_SECRET = "course-callback-signing-secret";

export function settingsFromEnvironment(): Settings {
  const rawRelease = process.env["SERVICE_RELEASE"] ?? "1.0";
  if (rawRelease !== "1.0" && rawRelease !== "1.1") {
    throw new Error("SERVICE_RELEASE must be 1.0 or 1.1");
  }

  const settings: Settings = {
    databaseUrl:
      process.env["DATABASE_URL"] ??
      "postgresql://analysis:analysis@127.0.0.1:55432/analysis_typescript",
    artifactRoot: resolve(
      process.env["ARTIFACT_ROOT"] ?? ".runtime/artifacts",
    ),
    remoteFixtureRoot: resolve(
      process.env["REMOTE_FIXTURE_ROOT"] ?? "fixtures/remote",
    ),
    webhookTransportBase: (
      process.env["WEBHOOK_TRANSPORT_BASE"] ?? "http://127.0.0.1:58080"
    ).replace(/\/$/, ""),
    webhookEncryptionKey:
      process.env["WEBHOOK_ENCRYPTION_KEY"] ?? COURSE_ENCRYPTION_KEY,
    callbackSigningSecret:
      process.env["CALLBACK_SIGNING_SECRET"] ?? COURSE_CALLBACK_SECRET,
    workerId:
      process.env["WORKER_ID"] ?? `typescript-worker-${process.pid}`,
    workerLeaseSeconds: positiveInteger("WORKER_LEASE_SECONDS", 15),
    uploadLimitBytes: positiveInteger("UPLOAD_LIMIT_BYTES", 1_048_576),
    serviceRelease: rawRelease,
    publicApiVersion: rawRelease === "1.1" ? "1.2.0" : "1.1.0",
    environment: process.env["APP_ENV"] ?? "development",
  };

  if (settings.workerLeaseSeconds < 5) {
    throw new Error("WORKER_LEASE_SECONDS must be at least 5");
  }
  if (settings.uploadLimitBytes !== 1_048_576) {
    throw new Error("UPLOAD_LIMIT_BYTES must match the frozen 1 MiB contract");
  }
  if (settings.webhookEncryptionKey.length < 20) {
    throw new Error("WEBHOOK_ENCRYPTION_KEY must contain at least 20 characters");
  }
  if (settings.callbackSigningSecret.length < 20) {
    throw new Error("CALLBACK_SIGNING_SECRET must contain at least 20 characters");
  }
  if (settings.environment === "production") {
    if (settings.webhookEncryptionKey === COURSE_ENCRYPTION_KEY) {
      throw new Error("the course encryption key is forbidden in production");
    }
    if (settings.callbackSigningSecret === COURSE_CALLBACK_SECRET) {
      throw new Error("the course callback secret is forbidden in production");
    }
  }

  mkdirSync(settings.artifactRoot, { recursive: true });
  mkdirSync(settings.remoteFixtureRoot, { recursive: true });
  return settings;
}

function positiveInteger(name: string, fallback: number): number {
  const raw = process.env[name] ?? String(fallback);
  if (!/^[1-9][0-9]*$/.test(raw)) {
    throw new Error(`${name} must be a positive integer`);
  }
  const value = Number(raw);
  if (!Number.isSafeInteger(value)) {
    throw new Error(`${name} exceeds JavaScript safe-integer precision`);
  }
  return value;
}
