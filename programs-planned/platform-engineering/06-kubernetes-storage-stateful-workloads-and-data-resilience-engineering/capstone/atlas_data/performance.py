from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StorageWorkload:
    iops: float
    average_kib: float
    p99_latency_ms: float
    queue_depth: float

    @property
    def throughput_mib_s(self) -> float:
        return self.iops * self.average_kib / 1024.0

    def within_budget(self, max_p99_ms: float, max_queue_depth: float) -> bool:
        return self.p99_latency_ms <= max_p99_ms and self.queue_depth <= max_queue_depth

    @property
    def average_outstanding_seconds(self) -> float:
        if self.iops <= 0:
            return 0.0
        return self.queue_depth / self.iops
