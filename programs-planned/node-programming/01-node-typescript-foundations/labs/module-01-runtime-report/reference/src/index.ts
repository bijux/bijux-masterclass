export interface RuntimeVersion {
  readonly major: number;
  readonly minor: number;
  readonly patch: number;
}

export interface RuntimeReport {
  readonly version: RuntimeVersion;
  readonly supported: boolean;
  readonly platform: string;
  readonly architecture: string;
  readonly executable: string;
  readonly moduleMode: 'esm';
}

export interface RuntimeInput {
  readonly version: string;
  readonly platform: string;
  readonly architecture: string;
  readonly executable: string;
  readonly moduleMode: 'esm';
}

export function isSupportedMajor(major: number): boolean {
  return Number.isSafeInteger(major) && major >= 24;
}

function parseComponent(raw: string, label: string): number {
  const value = Number(raw);
  if (!Number.isSafeInteger(value) || value < 0) {
    throw new Error(`${label} must be a nonnegative safe integer`);
  }
  return value;
}

export function parseNodeVersion(raw: string): RuntimeVersion {
  const match = /^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/.exec(raw);
  if (match === null) {
    throw new Error(`invalid Node version: ${raw}`);
  }
  const majorText = match[1];
  const minorText = match[2];
  const patchText = match[3];
  if (majorText === undefined || minorText === undefined || patchText === undefined) {
    throw new Error('version parser invariant failed');
  }
  return {
    major: parseComponent(majorText, 'major'),
    minor: parseComponent(minorText, 'minor'),
    patch: parseComponent(patchText, 'patch'),
  };
}

export function buildRuntimeReport(input: RuntimeInput): RuntimeReport {
  const version = parseNodeVersion(input.version);
  return {
    version,
    supported: isSupportedMajor(version.major),
    platform: input.platform,
    architecture: input.architecture,
    executable: input.executable,
    moduleMode: input.moduleMode,
  };
}

export function renderRuntimeReport(report: RuntimeReport): string {
  const version = `v${report.version.major}.${report.version.minor}.${report.version.patch}`;
  return [
    `version\t${version}`,
    `major\t${report.version.major}`,
    `supported\t${report.supported}`,
    `platform\t${report.platform}`,
    `architecture\t${report.architecture}`,
    `executable\t${report.executable}`,
    `module-mode\t${report.moduleMode}`,
  ].join('\n') + '\n';
}
