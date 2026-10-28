import { randomUUID } from "node:crypto";
import { partitionFor } from "./partitioning.js";
import type { EventEnvelope } from "./envelope.js";

export interface RecordEntry {
  readonly channel: string;
  readonly partition: number;
  readonly offset: string;
  readonly key: string;
  readonly event: EventEnvelope;
  readonly publishedAtMs: number;
}

export interface Delivery {
  readonly token: string;
  readonly group: string;
  readonly record: RecordEntry;
  readonly attempt: number;
  readonly deadlineMs: number;
}

interface GroupState {
  nextOffsets: bigint[];
  inflight: Map<number, Delivery>;
  attempts: Map<string, number>;
  availableAfter: Map<string, number>;
  terminated: Set<string>;
}

export class BrokerError extends Error {}

export class DeterministicBroker {
  private readonly channels = new Map<string, RecordEntry[][]>();
  private readonly groups = new Map<string, GroupState>();
  private readonly tokens = new Map<string, { group: string; channel: string; partition: number }>();
  private readonly roundRobin = new Map<string, number>();

  constructor(private readonly clock: () => number = () => Date.now()) {}

  createChannel(name: string, partitions: number): void {
    if (!name || !Number.isSafeInteger(partitions) || partitions <= 0) throw new Error("invalid channel");
    if (this.channels.has(name)) throw new BrokerError(`channel already exists: ${name}`);
    this.channels.set(name, Array.from({ length: partitions }, () => []));
  }

  publish(channel: string, key: string, event: EventEnvelope): RecordEntry {
    const target = this.channels.get(channel);
    if (!target) throw new BrokerError(`unknown channel: ${channel}`);
    if (event.partitionkey !== key) throw new BrokerError("transport key and envelope partitionkey differ");
    const partition = partitionFor(key, target.length);
    const log = target[partition];
    if (!log) throw new BrokerError("partition missing");
    const record: RecordEntry = Object.freeze({
      channel,
      partition,
      offset: String(log.length),
      key,
      event,
      publishedAtMs: this.clock(),
    });
    log.push(record);
    return record;
  }

  private state(group: string, channel: string): GroupState {
    const target = this.channels.get(channel);
    if (!target) throw new BrokerError(`unknown channel: ${channel}`);
    const identity = `${group}\u0000${channel}`;
    let value = this.groups.get(identity);
    if (!value) {
      value = {
        nextOffsets: Array.from({ length: target.length }, () => 0n),
        inflight: new Map(),
        attempts: new Map(),
        availableAfter: new Map(),
        terminated: new Set(),
      };
      this.groups.set(identity, value);
    }
    return value;
  }

  poll(group: string, channel: string, maxMessages = 1, ackWaitMs = 30_000): Delivery[] {
    if (!Number.isSafeInteger(maxMessages) || maxMessages <= 0 || ackWaitMs <= 0) throw new Error("invalid poll bounds");
    const target = this.channels.get(channel);
    if (!target) throw new BrokerError(`unknown channel: ${channel}`);
    const state = this.state(group, channel);
    const now = this.clock();
    for (const [partition, delivery] of [...state.inflight.entries()]) {
      if (delivery.deadlineMs <= now) state.inflight.delete(partition);
    }
    const groupKey = `${group}\u0000${channel}`;
    const start = this.roundRobin.get(groupKey) ?? 0;
    const deliveries: Delivery[] = [];
    for (let step = 0; step < target.length && deliveries.length < maxMessages; step += 1) {
      const partition = (start + step) % target.length;
      if (state.inflight.has(partition)) continue;
      const offset = state.nextOffsets[partition] ?? 0n;
      const log = target[partition];
      const record = log?.[Number(offset)];
      if (!record) continue;
      const position = `${partition}:${offset}`;
      if (state.terminated.has(position)) {
        state.nextOffsets[partition] = offset + 1n;
        continue;
      }
      if ((state.availableAfter.get(position) ?? now) > now) continue;
      const attempt = (state.attempts.get(position) ?? 0) + 1;
      state.attempts.set(position, attempt);
      const delivery: Delivery = Object.freeze({
        token: randomUUID(), group, record, attempt, deadlineMs: now + ackWaitMs,
      });
      state.inflight.set(partition, delivery);
      this.tokens.set(delivery.token, { group, channel, partition });
      deliveries.push(delivery);
    }
    if (target.length) this.roundRobin.set(groupKey, (start + 1) % target.length);
    return deliveries;
  }

  private take(token: string): { state: GroupState; delivery: Delivery } {
    const identity = this.tokens.get(token);
    if (!identity) throw new BrokerError("unknown or already-settled delivery token");
    this.tokens.delete(token);
    const state = this.state(identity.group, identity.channel);
    const delivery = state.inflight.get(identity.partition);
    if (!delivery || delivery.token !== token) throw new BrokerError("delivery token is stale");
    state.inflight.delete(identity.partition);
    return { state, delivery };
  }

  ack(token: string): void {
    const { state, delivery } = this.take(token);
    const partition = delivery.record.partition;
    const expected = state.nextOffsets[partition] ?? 0n;
    if (String(expected) !== delivery.record.offset) throw new BrokerError("offset is not current");
    state.nextOffsets[partition] = expected + 1n;
    state.availableAfter.delete(`${partition}:${expected}`);
  }

  nack(token: string, delayMs: number): void {
    if (delayMs < 0) throw new Error("negative delay");
    const { state, delivery } = this.take(token);
    state.availableAfter.set(`${delivery.record.partition}:${delivery.record.offset}`, this.clock() + delayMs);
  }

  term(token: string): void {
    const { state, delivery } = this.take(token);
    const partition = delivery.record.partition;
    const offset = BigInt(delivery.record.offset);
    state.terminated.add(`${partition}:${offset}`);
    state.nextOffsets[partition] = offset + 1n;
  }

  records(channel: string): RecordEntry[] {
    const target = this.channels.get(channel);
    if (!target) throw new BrokerError(`unknown channel: ${channel}`);
    return target.flat();
  }
}
