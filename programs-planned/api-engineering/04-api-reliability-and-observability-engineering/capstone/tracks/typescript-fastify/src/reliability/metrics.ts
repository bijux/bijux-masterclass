export class MetricError extends Error {}

export interface MetricDescriptor {
  readonly name: string;
  readonly description: string;
  readonly unit: string;
  readonly labels?: readonly string[];
  readonly maxSeries?: number;
}

type LabelKey = string;
const METRIC_NAME = /^[a-zA-Z_:][a-zA-Z0-9_:]*$/;
const LABEL_NAME = /^[a-zA-Z_][a-zA-Z0-9_]*$/;
const FORBIDDEN_IDENTIFIER_LABELS = new Set([
  "user_id", "tenant_id", "project_id", "dataset_id", "run_id",
  "artifact_id", "request_id", "trace_id", "span_id",
]);

function validateDescriptor(descriptor: MetricDescriptor): void {
  if (!METRIC_NAME.test(descriptor.name)) {
    throw new MetricError(`invalid metric name ${descriptor.name}`);
  }
  if (descriptor.description.trim() === "") {
    throw new MetricError("metric description must not be empty");
  }
  const labels = [...(descriptor.labels ?? [])];
  if (new Set(labels).size !== labels.length ||
      labels.some((label) => !LABEL_NAME.test(label))) {
    throw new MetricError("metric labels must be unique valid names");
  }
  if (labels.some((label) => FORBIDDEN_IDENTIFIER_LABELS.has(label))) {
    throw new MetricError("metric labels contain a forbidden identifier");
  }
  const maximum = descriptor.maxSeries ?? 100;
  if (!Number.isSafeInteger(maximum) || maximum < 1) {
    throw new MetricError("maxSeries must be a positive safe integer");
  }
}

function labelKey(
  descriptor: MetricDescriptor,
  labels: Readonly<Record<string, string>> = {},
): LabelKey {
  const names = [...(descriptor.labels ?? [])];
  const supplied = Object.keys(labels).sort();
  if (JSON.stringify([...names].sort()) !== JSON.stringify(supplied)) {
    throw new MetricError(`metric ${descriptor.name} label mismatch`);
  }
  const values = names.map((name) => String(labels[name]));
  if (values.some((value) => value.length > 120)) {
    throw new MetricError("metric label value exceeds 120 characters");
  }
  return values.join("\u0000");
}

function valuesFromKey(key: LabelKey): string[] {
  return key === "" ? [] : key.split("\u0000");
}

function guard(
  descriptor: MetricDescriptor,
  values: Map<LabelKey, unknown>,
  key: LabelKey,
): void {
  if (!values.has(key) && values.size >= (descriptor.maxSeries ?? 100)) {
    throw new MetricError(
      `metric ${descriptor.name} exceeded its series budget`,
    );
  }
}

export class Counter {
  public readonly values = new Map<LabelKey, number>();
  public constructor(public readonly descriptor: MetricDescriptor) {
    validateDescriptor(descriptor);
  }
  public add(
    amount = 1,
    labels: Readonly<Record<string, string>> = {},
  ): void {
    if (!Number.isFinite(amount) || amount < 0) {
      throw new MetricError(
        "counter increment must be finite and non-negative",
      );
    }
    const key = labelKey(this.descriptor, labels);
    guard(this.descriptor, this.values, key);
    this.values.set(key, (this.values.get(key) ?? 0) + amount);
  }
}

export class Gauge {
  public readonly values = new Map<LabelKey, number>();
  public constructor(public readonly descriptor: MetricDescriptor) {
    validateDescriptor(descriptor);
  }
  public set(
    value: number,
    labels: Readonly<Record<string, string>> = {},
  ): void {
    if (!Number.isFinite(value)) {
      throw new MetricError("gauge must be finite");
    }
    const key = labelKey(this.descriptor, labels);
    guard(this.descriptor, this.values, key);
    this.values.set(key, value);
  }
}

export interface HistogramPoint {
  count: number;
  total: number;
  /** Cumulative counts for each boundary plus +Inf. */
  buckets: number[];
}

export class Histogram {
  public readonly values = new Map<LabelKey, HistogramPoint>();
  public constructor(
    public readonly descriptor: MetricDescriptor,
    public readonly boundaries: readonly number[],
  ) {
    validateDescriptor(descriptor);
    if (boundaries.some((value) => !Number.isFinite(value))) {
      throw new MetricError("boundaries must be finite");
    }
    if (new Set(boundaries).size !== boundaries.length ||
        JSON.stringify([...boundaries].sort((a, b) => a - b)) !==
          JSON.stringify(boundaries)) {
      throw new MetricError("boundaries must be sorted and unique");
    }
  }
  public observe(
    value: number,
    labels: Readonly<Record<string, string>> = {},
  ): void {
    if (!Number.isFinite(value)) {
      throw new MetricError("observation must be finite");
    }
    const key = labelKey(this.descriptor, labels);
    guard(this.descriptor, this.values, key);
    const point = this.values.get(key) ?? {
      count: 0,
      total: 0,
      buckets: Array(this.boundaries.length + 1).fill(0) as number[],
    };
    point.count += 1;
    point.total += value;
    for (let index = 0; index < this.boundaries.length; index += 1) {
      if (value <= (this.boundaries[index] as number)) {
        point.buckets[index] = (point.buckets[index] ?? 0) + 1;
      }
    }
    const infinity = point.buckets.length - 1;
    point.buckets[infinity] = (point.buckets[infinity] ?? 0) + 1;
    this.values.set(key, point);
  }
}

export class MetricRegistry {
  private readonly registered = new Map<string, Counter | Gauge | Histogram>();
  public counter(descriptor: MetricDescriptor): Counter {
    const value = new Counter(descriptor);
    this.register(value);
    return value;
  }
  public gauge(descriptor: MetricDescriptor): Gauge {
    const value = new Gauge(descriptor);
    this.register(value);
    return value;
  }
  public histogram(
    descriptor: MetricDescriptor,
    boundaries: readonly number[],
  ): Histogram {
    const value = new Histogram(descriptor, boundaries);
    this.register(value);
    return value;
  }
  public get(name: string): Counter | Gauge | Histogram {
    const value = this.registered.get(name);
    if (value === undefined) throw new MetricError(`unknown metric ${name}`);
    return value;
  }
  public metrics(): readonly (Counter | Gauge | Histogram)[] {
    return [...this.registered.entries()]
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([, value]) => value);
  }
  public renderPrometheus(): string {
    const lines: string[] = [];
    for (const metric of this.metrics()) {
      const descriptor = metric.descriptor;
      lines.push(`# HELP ${descriptor.name} ${escapeHelp(descriptor.description)}`);
      const kind = metric instanceof Counter
        ? "counter"
        : metric instanceof Gauge
        ? "gauge"
        : "histogram";
      lines.push(`# TYPE ${descriptor.name} ${kind}`);
      if (metric instanceof Counter || metric instanceof Gauge) {
        for (const [key, value] of [...metric.values].sort(([a], [b]) => a.localeCompare(b))) {
          const labels = formatLabels(descriptor.labels ?? [], valuesFromKey(key));
          lines.push(`${descriptor.name}${labels} ${number(value)}`);
        }
      } else {
        for (const [key, point] of [...metric.values].sort(([a], [b]) => a.localeCompare(b))) {
          const values = valuesFromKey(key);
          for (let index = 0; index < point.buckets.length; index += 1) {
            const le = index === metric.boundaries.length
              ? "+Inf"
              : number(metric.boundaries[index] as number);
            const labels = formatLabels(
              descriptor.labels ?? [],
              values,
              ["le", le],
            );
            lines.push(`${descriptor.name}_bucket${labels} ${point.buckets[index]}`);
          }
          const base = formatLabels(descriptor.labels ?? [], values);
          lines.push(`${descriptor.name}_count${base} ${point.count}`);
          lines.push(`${descriptor.name}_sum${base} ${number(point.total)}`);
        }
      }
    }
    lines.push("# EOF");
    return `${lines.join("\n")}\n`;
  }
  private register(value: Counter | Gauge | Histogram): void {
    if (this.registered.has(value.descriptor.name)) {
      throw new MetricError(`duplicate metric ${value.descriptor.name}`);
    }
    this.registered.set(value.descriptor.name, value);
  }
}

function escapeHelp(value: string): string {
  return value.replaceAll("\\", "\\\\").replaceAll("\n", "\\n");
}
function escapeLabel(value: string): string {
  return value
    .replaceAll("\\", "\\\\")
    .replaceAll("\n", "\\n")
    .replaceAll('"', '\\"');
}
function formatLabels(
  names: readonly string[],
  values: readonly string[],
  extra?: readonly [string, string],
): string {
  const pairs = names.map(
    (name, index) => `${name}="${escapeLabel(values[index] ?? "")}"`,
  );
  if (extra !== undefined) {
    pairs.push(`${extra[0]}="${escapeLabel(extra[1])}"`);
  }
  return pairs.length === 0 ? "" : `{${pairs.join(",")}}`;
}
function number(value: number): string {
  return String(value);
}
