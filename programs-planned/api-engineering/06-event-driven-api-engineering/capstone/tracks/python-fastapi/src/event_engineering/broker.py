from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Callable
from uuid import uuid4

from .envelope import EventEnvelope
from .partitioning import partition_for


@dataclass(frozen=True, slots=True)
class Record:
    channel: str
    partition: int
    offset: int
    key: str
    event: EventEnvelope
    published_at: datetime


@dataclass(frozen=True, slots=True)
class Delivery:
    token: str
    group: str
    record: Record
    attempt: int
    deadline: datetime


@dataclass(slots=True)
class _Inflight:
    delivery: Delivery


@dataclass(slots=True)
class _GroupState:
    next_offsets: dict[int, int]
    inflight: dict[int, _Inflight] = field(default_factory=dict)
    attempts: dict[tuple[int, int], int] = field(default_factory=dict)
    available_after: dict[tuple[int, int], datetime] = field(default_factory=dict)
    terminated: set[tuple[int, int]] = field(default_factory=set)


@dataclass(slots=True)
class _Channel:
    partitions: list[list[Record]]


class BrokerError(RuntimeError):
    pass


class DeterministicBroker:
    """Single-process semantic model with deterministic clocks."""

    def __init__(self, clock: Callable[[], datetime] | None = None) -> None:
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._channels: dict[str, _Channel] = {}
        self._groups: dict[tuple[str, str], _GroupState] = {}
        self._tokens: dict[str, tuple[str, str, int]] = {}
        self._round_robin: dict[tuple[str, str], int] = {}

    def create_channel(self, name: str, partitions: int) -> None:
        if not name or partitions <= 0:
            raise ValueError("channel name and positive partition count required")
        if name in self._channels:
            raise BrokerError(f"channel already exists: {name}")
        self._channels[name] = _Channel([[] for _ in range(partitions)])

    def publish(self, channel: str, key: str, event: EventEnvelope) -> Record:
        target = self._channels.get(channel)
        if target is None:
            raise BrokerError(f"unknown channel: {channel}")
        if event.partitionkey != key:
            raise BrokerError("transport key and envelope partitionkey differ")
        partition = partition_for(key, len(target.partitions))
        offset = len(target.partitions[partition])
        record = Record(
            channel=channel,
            partition=partition,
            offset=offset,
            key=key,
            event=event,
            published_at=self._clock(),
        )
        target.partitions[partition].append(record)
        return record

    def _state(self, group: str, channel: str) -> _GroupState:
        if channel not in self._channels:
            raise BrokerError(f"unknown channel: {channel}")
        identity = (group, channel)
        if identity not in self._groups:
            count = len(self._channels[channel].partitions)
            self._groups[identity] = _GroupState(
                {index: 0 for index in range(count)}
            )
        return self._groups[identity]

    def poll(
        self,
        group: str,
        channel: str,
        *,
        max_messages: int = 1,
        ack_wait: timedelta = timedelta(seconds=30),
    ) -> list[Delivery]:
        if max_messages <= 0 or ack_wait.total_seconds() <= 0:
            raise ValueError("positive max_messages and ack_wait required")
        target = self._channels.get(channel)
        if target is None:
            raise BrokerError(f"unknown channel: {channel}")
        state = self._state(group, channel)
        now = self._clock()
        for partition, inflight in list(state.inflight.items()):
            if inflight.delivery.deadline <= now:
                del state.inflight[partition]
        count = len(target.partitions)
        start = self._round_robin.get((group, channel), 0)
        deliveries: list[Delivery] = []
        for step in range(count):
            if len(deliveries) >= max_messages:
                break
            partition = (start + step) % count
            if partition in state.inflight:
                continue
            offset = state.next_offsets[partition]
            log = target.partitions[partition]
            if offset >= len(log):
                continue
            position = (partition, offset)
            if position in state.terminated:
                state.next_offsets[partition] += 1
                continue
            if state.available_after.get(position, now) > now:
                continue
            attempt = state.attempts.get(position, 0) + 1
            state.attempts[position] = attempt
            token = str(uuid4())
            delivery = Delivery(
                token=token,
                group=group,
                record=log[offset],
                attempt=attempt,
                deadline=now + ack_wait,
            )
            state.inflight[partition] = _Inflight(delivery)
            self._tokens[token] = (group, channel, partition)
            deliveries.append(delivery)
        if count:
            self._round_robin[(group, channel)] = (start + 1) % count
        return deliveries

    def _take(self, token: str) -> tuple[_GroupState, Delivery]:
        identity = self._tokens.pop(token, None)
        if identity is None:
            raise BrokerError("unknown or already-settled delivery token")
        group, channel, partition = identity
        state = self._state(group, channel)
        inflight = state.inflight.pop(partition, None)
        if inflight is None or inflight.delivery.token != token:
            raise BrokerError("delivery token is stale")
        return state, inflight.delivery

    def ack(self, token: str) -> None:
        state, delivery = self._take(token)
        partition = delivery.record.partition
        expected = state.next_offsets[partition]
        if expected != delivery.record.offset:
            raise BrokerError("acknowledgement offset is not current")
        state.next_offsets[partition] += 1
        state.available_after.pop((partition, expected), None)

    def nack(self, token: str, delay: timedelta) -> None:
        if delay.total_seconds() < 0:
            raise ValueError("negative delay")
        state, delivery = self._take(token)
        state.available_after[
            (delivery.record.partition, delivery.record.offset)
        ] = self._clock() + delay

    def term(self, token: str) -> None:
        state, delivery = self._take(token)
        position = (delivery.record.partition, delivery.record.offset)
        state.terminated.add(position)
        state.next_offsets[delivery.record.partition] += 1

    def records(self, channel: str) -> list[Record]:
        target = self._channels[channel]
        return [record for partition in target.partitions for record in partition]

    def lag(self, group: str, channel: str) -> tuple[int, int]:
        target = self._channels[channel]
        state = self._state(group, channel)
        count = 0
        oldest_age = 0
        now = self._clock()
        for partition, log in enumerate(target.partitions):
            start = state.next_offsets[partition]
            pending = log[start:]
            count += len(pending)
            if pending:
                age = int((now - pending[0].published_at).total_seconds())
                oldest_age = max(oldest_age, max(age, 0))
        return count, oldest_age
