import type { EventEnvelope } from "./envelope.js";

export interface WindowResult { tenantId: string; startMs: number; endMs: number; completed: number; failed: number; durationMs: number; revision: number }
export interface LateEvent { eventId: string; tenantId: string; eventTimeMs: number; watermarkMs: number; reason: string }

export class EventTimeWindows {
  private watermarkMs = Number.MIN_SAFE_INTEGER;
  private readonly windows = new Map<string, { tenantId: string; startMs: number; completed: number; failed: number; durationMs: number; revision: number }>();
  private readonly seen = new Set<string>();
  readonly lateEvents: LateEvent[] = [];

  constructor(private readonly widthMs: number, private readonly allowedLatenessMs: number) {
    if (!Number.isSafeInteger(widthMs) || widthMs <= 0 || allowedLatenessMs < 0) throw new Error("invalid window policy");
  }

  advanceWatermark(valueMs: number): void {
    if (!Number.isSafeInteger(valueMs) || valueMs < this.watermarkMs) throw new Error("invalid watermark");
    this.watermarkMs = valueMs;
  }

  apply(event: EventEnvelope): WindowResult | null {
    if (this.seen.has(event.id)) return null;
    const raw = event.data.occurredAt ?? event.time;
    if (typeof raw !== "string") throw new Error("event time must be text");
    const eventTimeMs = Date.parse(raw);
    if (!Number.isSafeInteger(eventTimeMs)) throw new Error("invalid event time");
    const threshold = this.watermarkMs === Number.MIN_SAFE_INTEGER ? this.watermarkMs : this.watermarkMs - this.allowedLatenessMs;
    if (eventTimeMs < threshold) {
      this.lateEvents.push({ eventId: event.id, tenantId: event.tenantid, eventTimeMs, watermarkMs: this.watermarkMs, reason: "beyond-allowed-lateness" });
      this.seen.add(event.id);
      return null;
    }
    const startMs = eventTimeMs - (eventTimeMs % this.widthMs);
    const key = `${event.tenantid}\u0000${startMs}`;
    const row = this.windows.get(key) ?? { tenantId: event.tenantid, startMs, completed: 0, failed: 0, durationMs: 0, revision: 0 };
    if (event.type.endsWith("run.completed.v1")) {
      row.completed += 1;
      row.durationMs += Number(event.data.durationMs ?? 0);
    } else if (event.type.endsWith("run.failed.v1")) row.failed += 1;
    else return null;
    row.revision += 1;
    this.windows.set(key, row);
    this.seen.add(event.id);
    return { ...row, endMs: startMs + this.widthMs };
  }

  snapshot(): WindowResult[] {
    return [...this.windows.values()].sort((a, b) => a.startMs - b.startMs || a.tenantId.localeCompare(b.tenantId)).map((row) => ({ ...row, endMs: row.startMs + this.widthMs }));
  }
}
