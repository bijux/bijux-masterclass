import type { JobView } from './domain.js';
import type { RuntimeEndpoints, RuntimeTerminalReport } from './runtime.js';
import type { ServiceStats, SubmissionResult } from './service.js';

export const HELP = `ServiceWire — bounded network-service engineering reference

Commands:
  servicewire serve [--host <host>] [--port <port>] [--http2-port <port>] [--discovery-port <port>]
  servicewire submit --url <base-url> --key <key> --operation <name> --payload <text>
  servicewire get --url <base-url> <job-id>
  servicewire stats --url <base-url>
  servicewire discover [--host <host>] --port <port>
  servicewire demo
  servicewire help
  servicewire version
`;

export function renderJson(value: unknown): string {
  return `${JSON.stringify(value, null, 2)}\n`;
}

export function renderEndpoints(endpoints: RuntimeEndpoints): string {
  const lines = ['servicewire ready'];
  if (endpoints.http) lines.push(`http ${endpoints.http}`);
  if (endpoints.https) lines.push(`https ${endpoints.https}`);
  if (endpoints.http2) lines.push(`http2 ${endpoints.http2}`);
  if (endpoints.discovery) lines.push(`discovery ${endpoints.discovery.host}:${endpoints.discovery.port}`);
  return `${lines.join('\n')}\n`;
}

export function renderSubmission(result: SubmissionResult): string {
  return `job ${result.job.id} state=${result.job.state} revision=${result.job.revision} replay=${result.replay}\n`;
}

export function renderJob(job: JobView): string {
  const suffix = job.result !== undefined
    ? ` result=${JSON.stringify(job.result)}`
    : job.error !== undefined
      ? ` error=${job.error.code}:${JSON.stringify(job.error.message)}`
      : '';
  return `job ${job.id} operation=${job.operation} state=${job.state} revision=${job.revision}${suffix}\n`;
}

export function renderStats(stats: ServiceStats): string {
  return `state=${stats.state} readiness=${stats.readiness} queued=${stats.queued} active=${stats.active} jobs=${stats.retainedJobs} subscribers=${stats.subscribers}\n`;
}

export function renderTerminal(report: RuntimeTerminalReport): string {
  const app = report.application;
  return `shutdown accepted=${app.acceptedJobs} succeeded=${app.succeededJobs} failed=${app.failedJobs} cancelled=${app.cancelledJobs} cleanup-errors=${report.cleanupErrors.length}\n`;
}
