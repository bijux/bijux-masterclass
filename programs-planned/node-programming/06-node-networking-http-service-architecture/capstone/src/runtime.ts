import type { RuntimeConfig } from './config.js';
import { validateLimits, validateListenConfig } from './config.js';
import { startDiscoveryServer } from './discovery.js';
import { startHttp1Server } from './http1.js';
import { startHttp2Server } from './http2.js';
import { ServiceWireApplication, type ServiceTerminalReport } from './service.js';

type Http1Handle = Awaited<ReturnType<typeof startHttp1Server>>;
type Http2Handle = Awaited<ReturnType<typeof startHttp2Server>>;
type DiscoveryHandle = Awaited<ReturnType<typeof startDiscoveryServer>>;

export interface RuntimeEndpoints {
  readonly http?: string;
  readonly https?: string;
  readonly http2?: string;
  readonly discovery?: { readonly host: string; readonly port: number };
}

export interface RuntimeTerminalReport {
  readonly application: ServiceTerminalReport;
  readonly cleanupErrors: readonly string[];
}

export interface ServiceWireRuntime {
  readonly application: ServiceWireApplication;
  readonly endpoints: RuntimeEndpoints;
  close(): Promise<RuntimeTerminalReport>;
}

function errorMessage(error: unknown): string {
  return error instanceof Error ? `${error.name}: ${error.message}` : String(error);
}

export async function startServiceWire(config: RuntimeConfig): Promise<ServiceWireRuntime> {
  const limits = validateLimits(config.limits);
  const application = new ServiceWireApplication(limits);
  let http: Http1Handle | undefined;
  let https: Http1Handle | undefined;
  let http2: Http2Handle | undefined;
  let discovery: DiscoveryHandle | undefined;

  try {
    if (config.http) {
      const listen = validateListenConfig(config.http);
      http = await startHttp1Server({ application, limits, ...listen });
    }
    if (config.https) {
      const listen = validateListenConfig(config.https);
      https = await startHttp1Server({ application, limits, ...listen, tls: config.https.tls });
    }
    if (config.http2) {
      const listen = validateListenConfig(config.http2);
      http2 = await startHttp2Server({ application, limits, ...listen });
    }
    if (config.discovery) {
      const listen = validateListenConfig(config.discovery);
      const advertisedUrl = config.advertisedUrl ?? http?.url ?? https?.url ?? http2?.authority;
      if (!advertisedUrl) throw new Error('discovery requires an advertised URL or an HTTP endpoint');
      new URL(advertisedUrl);
      discovery = await startDiscoveryServer({ ...listen, advertisedUrl });
    }
  } catch (error) {
    const cleanups: Promise<unknown>[] = [];
    if (discovery) cleanups.push(discovery.close());
    if (http2) cleanups.push(http2.close(0));
    if (https) cleanups.push(https.close(0));
    if (http) cleanups.push(http.close(0));
    cleanups.push(application.close(0));
    await Promise.allSettled(cleanups);
    throw error;
  }

  const endpoints: RuntimeEndpoints = {
    ...(http ? { http: http.url } : {}),
    ...(https ? { https: https.url } : {}),
    ...(http2 ? { http2: http2.authority } : {}),
    ...(discovery ? { discovery: { host: discovery.host, port: discovery.port } } : {}),
  };

  let closePromise: Promise<RuntimeTerminalReport> | undefined;
  const close = (): Promise<RuntimeTerminalReport> => {
    if (closePromise) return closePromise;
    closePromise = (async () => {
      application.quiesce();
      const operations: Promise<unknown>[] = [application.close(limits.shutdownGraceMs)];
      if (discovery) operations.push(discovery.close());
      if (http) operations.push(http.close(limits.shutdownGraceMs));
      if (https) operations.push(https.close(limits.shutdownGraceMs));
      if (http2) operations.push(http2.close(limits.shutdownGraceMs));
      const results = await Promise.allSettled(operations);
      const appResult = results[0];
      if (!appResult || appResult.status !== 'fulfilled') {
        throw appResult?.status === 'rejected' ? appResult.reason : new Error('application close did not produce a result');
      }
      return {
        application: appResult.value as ServiceTerminalReport,
        cleanupErrors: results.slice(1)
          .filter((result): result is PromiseRejectedResult => result.status === 'rejected')
          .map((result) => errorMessage(result.reason)),
      };
    })();
    return closePromise;
  };

  return { application, endpoints, close };
}
