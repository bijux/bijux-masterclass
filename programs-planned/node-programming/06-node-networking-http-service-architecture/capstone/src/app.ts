import { readFile } from 'node:fs/promises';
import { once } from 'node:events';
import type { Command } from './command.js';
import { defaultLimits } from './config.js';
import { discoverService } from './discovery.js';
import { ServiceWireClient } from './client.js';
import { startServiceWire } from './runtime.js';
import { HELP, renderEndpoints, renderJob, renderJson, renderStats, renderSubmission, renderTerminal } from './render.js';
import { SERVICEWIRE_VERSION } from './version.js';

export interface CommandResult {
  readonly stdout: string;
  readonly exitCode: number;
}

function clientFor(baseUrl: URL): ServiceWireClient {
  return new ServiceWireClient({
    baseUrl,
    maxSockets: 4,
    maxResponseBytes: defaultLimits.maxResponseBodyBytes,
    maxAttempts: 3,
  });
}

async function waitForShutdownSignal(signal?: AbortSignal): Promise<void> {
  if (signal?.aborted) return;
  if (signal) {
    await once(signal, 'abort');
    return;
  }
  const controller = new AbortController();
  const stop = () => controller.abort();
  process.once('SIGINT', stop);
  process.once('SIGTERM', stop);
  try { await once(controller.signal, 'abort'); }
  finally {
    process.off('SIGINT', stop);
    process.off('SIGTERM', stop);
  }
}

export async function executeCommand(command: Command, signal?: AbortSignal): Promise<CommandResult> {
  switch (command.kind) {
    case 'help': return { stdout: HELP, exitCode: 0 };
    case 'version': return { stdout: `servicewire ${SERVICEWIRE_VERSION}\n`, exitCode: 0 };
    case 'discover': {
      const found = await discoverService({ host: command.host, port: command.port, budgetMs: 500 });
      return { stdout: renderJson(found), exitCode: 0 };
    }
    case 'submit': {
      const client = clientFor(command.baseUrl);
      try {
        const result = await client.submit(
          { operation: command.operation, payload: command.payload },
          command.idempotencyKey,
        );
        return { stdout: renderSubmission(result), exitCode: 0 };
      } finally { client.close(); }
    }
    case 'get': {
      const client = clientFor(command.baseUrl);
      try {
        const found = await client.getJob(command.id);
        if (found.notModified) return { stdout: `not-modified ${found.etag}\n`, exitCode: 0 };
        return { stdout: renderJob(found.job), exitCode: 0 };
      } finally { client.close(); }
    }
    case 'stats': {
      const client = clientFor(command.baseUrl);
      try { return { stdout: renderStats(await client.stats()), exitCode: 0 }; }
      finally { client.close(); }
    }
    case 'serve': {
      const runtime = await startServiceWire({
        limits: defaultLimits,
        http: { host: command.host, port: command.port },
        ...(command.http2Port !== undefined ? { http2: { host: command.host, port: command.http2Port } } : {}),
        ...(command.discoveryPort !== undefined ? { discovery: { host: command.host, port: command.discoveryPort } } : {}),
      });
      const ready = renderEndpoints(runtime.endpoints);
      process.stdout.write(ready);
      await waitForShutdownSignal(signal);
      const report = await runtime.close();
      return { stdout: renderTerminal(report), exitCode: report.cleanupErrors.length === 0 ? 0 : 1 };
    }
    case 'demo': {
      const runtime = await startServiceWire({
        limits: { ...defaultLimits, heartbeatMs: 50, shutdownGraceMs: 500 },
        http: { host: '127.0.0.1', port: 0 },
        http2: { host: '127.0.0.1', port: 0 },
        discovery: { host: '127.0.0.1', port: 0 },
      });
      const baseUrl = new URL(runtime.endpoints.http ?? 'http://127.0.0.1');
      const client = clientFor(baseUrl);
      try {
        const first = await client.submit({ operation: 'uppercase', payload: 'network boundaries' }, 'demo-key-0001');
        const terminal = await client.waitForTerminal(first.job.id, 1_000);
        const second = await client.submit({ operation: 'word-count', payload: 'one two three' }, 'demo-key-0002');
        const terminal2 = await client.waitForTerminal(second.job.id, 1_000);
        const stats = await client.stats();
        const report = await runtime.close();
        return {
          stdout: [
            'servicewire demo',
            renderJob(terminal).trimEnd(),
            renderJob(terminal2).trimEnd(),
            renderStats(stats).trimEnd(),
            renderTerminal(report).trimEnd(),
            '',
          ].join('\n'),
          exitCode: 0,
        };
      } finally {
        client.close();
        await runtime.close();
      }
    }
  }
}

export async function loadCourseCertificate(): Promise<Buffer> {
  return readFile(new URL('../../fixtures/tls/ca-cert.pem', import.meta.url));
}
