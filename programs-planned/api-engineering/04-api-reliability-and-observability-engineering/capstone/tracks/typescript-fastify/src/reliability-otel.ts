import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";

export interface OTelSettings {
  readonly serviceName: string;
  readonly serviceVersion: string;
  readonly endpoint: string;
}

export async function startOpenTelemetry(settings: OTelSettings): Promise<NodeSDK> {
  const sdk = new NodeSDK({
    serviceName: settings.serviceName,
    traceExporter: new OTLPTraceExporter({ url: `${settings.endpoint}/v1/traces` }),
  });
  await sdk.start();
  return sdk;
}
