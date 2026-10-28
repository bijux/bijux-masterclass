import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const proto = path.resolve(
  here,
  "../../../contracts/proto/bijux/analysis/v1/analysis.proto",
);
const definition = protoLoader.loadSync(proto, {
  longs:String, enums:String, defaults:false, oneofs:true,
});
const loaded = grpc.loadPackageDefinition(definition) as any;
const api = loaded.bijux.analysis.v1;

export function createClients(target: string, token: string) {
  const credentials = grpc.credentials.createInsecure();
  const metadata = new grpc.Metadata();
  metadata.set("authorization", `Bearer ${token}`);
  return {
    control:new api.AnalysisControlService(target, credentials),
    transfer:new api.DatasetTransferService(target, credentials),
    worker:new api.WorkerPlaneService(target, credentials),
    metadata,
  };
}
