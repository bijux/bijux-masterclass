import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import path from "node:path";
import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";

import { AnalysisStore } from "../src/inprocess.js";
import { authenticate, requireScope, requireTenant } from "../src/security.js";
import { etag, type AnalysisRun } from "../src/model.js";
import { parseUpload, type UploadFrame } from "../src/stream.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const proto = path.resolve(
  here,
  "../../../contracts/proto/bijux/analysis/v1/analysis.proto",
);
const definition = protoLoader.loadSync(proto, {
  longs: String,
  enums: String,
  defaults: false,
  oneofs: true,
  keepCase: false,
});
const loaded = grpc.loadPackageDefinition(definition) as any;
const api = loaded.bijux.analysis.v1;

function metadataTokens(metadata: grpc.Metadata): string[] {
  return metadata.get("authorization").map(String);
}

function runMessage(run: AnalysisRun): Record<string, unknown> {
  return {
    name: run.name,
    projectName: run.projectName,
    datasetName: run.datasetName,
    state: `RUN_STATE_${run.state}`,
    progressPercent: run.progressPercent,
    etag: etag(run),
    revision: run.revision.toString(),
    ...(run.resultSummary === undefined ? {} : { resultSummary: run.resultSummary }),
    ...(run.failureCode === undefined ? {} : { failureCode: run.failureCode }),
  };
}

function serviceError(code: grpc.status, message: string): grpc.ServiceError {
  return Object.assign(new Error(message), { code, details: message });
}

export function createNetworkServer(): grpc.Server {
  const store = new AnalysisStore();
  const server = new grpc.Server({
    "grpc.max_receive_message_length": 3 * 1024 * 1024,
    "grpc.max_send_message_length": 3 * 1024 * 1024,
  });

  server.addService(api.AnalysisControlService.service, {
    createRun(call: any, callback: any) {
      try {
        const principal = authenticate(metadataTokens(call.metadata));
        requireScope(principal, "runs:write");
        requireTenant(principal, call.request.parent);
        const run = store.createRun({
          parent: call.request.parent,
          requestId: call.request.requestId,
          datasetName: call.request.datasetName,
          algorithm: call.request.algorithm,
          principal,
        });
        callback(null, runMessage(run));
      } catch (error) {
        callback(mapError(error));
      }
    },

    getRun(call: any, callback: any) {
      try {
        const principal = authenticate(metadataTokens(call.metadata));
        requireScope(principal, "runs:read");
        requireTenant(principal, call.request.name);
        callback(null, runMessage(store.getRun(call.request.name)));
      } catch (error) {
        callback(mapError(error));
      }
    },

    cancelRun(call: any, callback: any) {
      try {
        const principal = authenticate(metadataTokens(call.metadata));
        requireScope(principal, "runs:write");
        requireTenant(principal, call.request.name);
        callback(
          null,
          runMessage(store.cancelRun(call.request.name, call.request.etag)),
        );
      } catch (error) {
        callback(mapError(error));
      }
    },

    watchRun(call: any) {
      try {
        const principal = authenticate(metadataTokens(call.metadata));
        requireScope(principal, "runs:read");
        requireTenant(principal, call.request.name);
        const run = store.getRun(call.request.name);
        const sequence = BigInt(call.request.resumeAfterSequence ?? "0") + 1n;
        call.write({
          eventId: `evt-${sequence.toString()}`,
          runName: run.name,
          sequence: sequence.toString(),
          snapshot: runMessage(run),
          type: run.state.toLowerCase(),
        });
        call.end();
      } catch (error) {
        call.destroy(mapError(error));
      }
    },
  });

  server.addService(api.DatasetTransferService.service, {
    uploadDataset(call: any, callback: any) {
      const frames: UploadFrame[] = [];
      let principal: ReturnType<typeof authenticate>;
      try {
        principal = authenticate(metadataTokens(call.metadata));
        requireScope(principal, "datasets:write");
      } catch (error) {
        callback(mapError(error));
        return;
      }
      call.on("data", (frame: any) => {
        if (frame.frame === "metadata" || frame.metadata !== undefined) {
          frames.push({
            kind:"metadata",
            parent:frame.metadata.parent,
            requestId:frame.metadata.requestId,
            filename:frame.metadata.filename,
            mediaType:frame.metadata.mediaType,
            sha256:frame.metadata.sha256 ?? "",
            expectedSize:BigInt(frame.metadata.expectedSizeBytes ?? "0"),
          });
        } else {
          frames.push({kind:"chunk", data:new Uint8Array(frame.chunk)});
        }
      });
      call.on("end", () => {
        try {
          const parsed = parseUpload(frames);
          requireTenant(principal, parsed.metadata.parent);
          callback(null, {
            datasetName:`datasets/d-${parsed.sha256.slice(0,16)}`,
            sizeBytes:parsed.size.toString(),
            sha256:parsed.sha256,
          });
        } catch (error) {
          callback(mapError(error));
        }
      });
      call.on("error", (error: unknown) => callback(mapError(error)));
    },

    downloadArtifact(call: any) {
      try {
        const principal = authenticate(metadataTokens(call.metadata));
        requireScope(principal, "artifacts:read");
        if (principal.tenant !== "tenant-a") {
          throw new Error("PERMISSION_DENIED");
        }
        const body = new TextEncoder().encode("analysis-artifact\n");
        const digest = createHash("sha256").update(body).digest("hex");
        const chunkSize = 8;
        for (let offset = 0; offset < body.length; offset += chunkSize) {
          const data = body.slice(offset, offset + chunkSize);
          call.write({
            offset:String(offset),
            data,
            complete:offset + data.length === body.length,
            sha256:offset + data.length === body.length ? digest : "",
          });
        }
        call.end();
      } catch (error) {
        call.destroy(mapError(error));
      }
    },
  });

  server.addService(api.WorkerPlaneService.service, {
    work(call: any) {
      let established = false;
      call.on("data", (frame: any) => {
        try {
          const principal = authenticate(metadataTokens(call.metadata));
          requireScope(principal, "worker:connect");
          if (!established) {
            if (frame.payload !== "hello" && frame.hello === undefined) {
              throw new Error("INVALID_ARGUMENT");
            }
            if (frame.hello.workerId !== principal.subject ||
                frame.hello.tenantId !== principal.tenant) {
              throw new Error("PERMISSION_DENIED");
            }
            established = true;
            call.write({ heartbeatIntervalMs:"5000" });
          } else if (frame.payload === "hello" || frame.hello !== undefined) {
            throw new Error("INVALID_ARGUMENT");
          }
        } catch (error) {
          call.destroy(mapError(error));
        }
      });
      call.on("end", () => call.end());
    },
  });

  return server;
}

function mapError(error: unknown): grpc.ServiceError {
  const message = error instanceof Error ? error.message : "INTERNAL";
  const table: Record<string, grpc.status> = {
    INVALID_ARGUMENT:grpc.status.INVALID_ARGUMENT,
    NOT_FOUND:grpc.status.NOT_FOUND,
    UNAUTHENTICATED:grpc.status.UNAUTHENTICATED,
    PERMISSION_DENIED:grpc.status.PERMISSION_DENIED,
    FAILED_PRECONDITION:grpc.status.FAILED_PRECONDITION,
    ABORTED:grpc.status.ABORTED,
    ALREADY_EXISTS:grpc.status.ALREADY_EXISTS,
    RESOURCE_EXHAUSTED:grpc.status.RESOURCE_EXHAUSTED,
  };
  return serviceError(table[message] ?? grpc.status.INTERNAL, message);
}
