from __future__ import annotations

from dataclasses import dataclass, field
import math
import re
from typing import Iterable


class MetricError(ValueError):
    pass


_METRIC_NAME = re.compile(r"^[a-zA-Z_:][a-zA-Z0-9_:]*$")
_LABEL_NAME = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

_FORBIDDEN_IDENTIFIER_LABELS = frozenset(
    {
        "user_id",
        "tenant_id",
        "project_id",
        "dataset_id",
        "run_id",
        "artifact_id",
        "request_id",
        "trace_id",
        "span_id",
    }
)
LabelValues = tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MetricDescriptor:
    name: str
    description: str
    unit: str
    labels: tuple[str, ...] = ()
    max_series: int = 100

    def __post_init__(self) -> None:
        if not _METRIC_NAME.fullmatch(self.name):
            raise MetricError(f"invalid metric name {self.name!r}")
        if not self.description.strip():
            raise MetricError("metric description must not be empty")
        if self.max_series < 1:
            raise MetricError("max_series must be positive")
        if len(self.labels) != len(set(self.labels)):
            raise MetricError("metric labels must be unique")
        if any(not _LABEL_NAME.fullmatch(label) for label in self.labels):
            raise MetricError("invalid metric label name")
        if _FORBIDDEN_IDENTIFIER_LABELS.intersection(self.labels):
            raise MetricError("metric labels contain a forbidden identifier")


@dataclass(slots=True)
class Counter:
    descriptor: MetricDescriptor
    values: dict[LabelValues, float] = field(default_factory=dict)

    def add(
        self,
        amount: float = 1.0,
        *,
        labels: dict[str, str] | None = None,
    ) -> None:
        if not math.isfinite(amount) or amount < 0:
            raise MetricError("counter increments must be finite and non-negative")
        key = _label_key(self.descriptor, labels)
        _guard_series(self.descriptor, self.values, key)
        self.values[key] = self.values.get(key, 0.0) + amount


@dataclass(slots=True)
class Gauge:
    descriptor: MetricDescriptor
    values: dict[LabelValues, float] = field(default_factory=dict)

    def set(
        self,
        value: float,
        *,
        labels: dict[str, str] | None = None,
    ) -> None:
        if not math.isfinite(value):
            raise MetricError("gauge value must be finite")
        key = _label_key(self.descriptor, labels)
        _guard_series(self.descriptor, self.values, key)
        self.values[key] = value


@dataclass(slots=True)
class HistogramPoint:
    count: int
    total: float
    # Cumulative counts for each configured boundary plus +Inf.
    buckets: list[int]


@dataclass(slots=True)
class Histogram:
    descriptor: MetricDescriptor
    boundaries: tuple[float, ...]
    values: dict[LabelValues, HistogramPoint] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if tuple(sorted(self.boundaries)) != self.boundaries:
            raise MetricError("histogram boundaries must be sorted")
        if len(self.boundaries) != len(set(self.boundaries)):
            raise MetricError("histogram boundaries must be unique")
        if any(not math.isfinite(value) for value in self.boundaries):
            raise MetricError("histogram boundaries must be finite")

    def observe(
        self,
        value: float,
        *,
        labels: dict[str, str] | None = None,
    ) -> None:
        if not math.isfinite(value):
            raise MetricError("histogram observations must be finite")
        key = _label_key(self.descriptor, labels)
        _guard_series(self.descriptor, self.values, key)
        point = self.values.setdefault(
            key,
            HistogramPoint(
                count=0,
                total=0.0,
                buckets=[0] * (len(self.boundaries) + 1),
            ),
        )
        point.count += 1
        point.total += value
        for index, boundary in enumerate(self.boundaries):
            if value <= boundary:
                point.buckets[index] += 1
        point.buckets[-1] += 1


class MetricRegistry:
    def __init__(self) -> None:
        self._metrics: dict[str, Counter | Gauge | Histogram] = {}

    def counter(self, descriptor: MetricDescriptor) -> Counter:
        metric = Counter(descriptor)
        self._register(metric)
        return metric

    def gauge(self, descriptor: MetricDescriptor) -> Gauge:
        metric = Gauge(descriptor)
        self._register(metric)
        return metric

    def histogram(
        self,
        descriptor: MetricDescriptor,
        boundaries: Iterable[float],
    ) -> Histogram:
        metric = Histogram(descriptor, tuple(boundaries))
        self._register(metric)
        return metric

    def get(self, name: str) -> Counter | Gauge | Histogram:
        return self._metrics[name]

    def metrics(self) -> tuple[Counter | Gauge | Histogram, ...]:
        return tuple(self._metrics[name] for name in sorted(self._metrics))

    def render_prometheus(self) -> str:
        """Render deterministic Prometheus text exposition.

        The dependency-light registry is educational. Live proof still validates
        the target exporter/backend. Histogram bucket values are cumulative.
        """

        lines: list[str] = []
        for metric in self.metrics():
            descriptor = metric.descriptor
            lines.append(f"# HELP {descriptor.name} {_escape_help(descriptor.description)}")
            metric_type = (
                "counter"
                if isinstance(metric, Counter)
                else "gauge"
                if isinstance(metric, Gauge)
                else "histogram"
            )
            lines.append(f"# TYPE {descriptor.name} {metric_type}")
            if isinstance(metric, (Counter, Gauge)):
                for values, value in sorted(metric.values.items()):
                    labels = _format_labels(descriptor.labels, values)
                    lines.append(f"{descriptor.name}{labels} {_number(value)}")
            else:
                for values, point in sorted(metric.values.items()):
                    for index, count in enumerate(point.buckets):
                        le = (
                            "+Inf"
                            if index == len(metric.boundaries)
                            else _number(metric.boundaries[index])
                        )
                        labels = _format_labels(
                            descriptor.labels,
                            values,
                            extra=("le", le),
                        )
                        lines.append(
                            f"{descriptor.name}_bucket{labels} {count}"
                        )
                    base = _format_labels(descriptor.labels, values)
                    lines.append(f"{descriptor.name}_count{base} {point.count}")
                    lines.append(
                        f"{descriptor.name}_sum{base} {_number(point.total)}"
                    )
        lines.append("# EOF")
        return "\n".join(lines) + "\n"

    def _register(self, metric: Counter | Gauge | Histogram) -> None:
        name = metric.descriptor.name
        if name in self._metrics:
            raise MetricError(f"duplicate metric {name}")
        self._metrics[name] = metric


def _label_key(
    descriptor: MetricDescriptor,
    labels: dict[str, str] | None,
) -> LabelValues:
    supplied = labels or {}
    if set(supplied) != set(descriptor.labels):
        raise MetricError(
            f"metric {descriptor.name} requires labels {descriptor.labels}, "
            f"received {tuple(sorted(supplied))}"
        )
    values = tuple(str(supplied[name]) for name in descriptor.labels)
    if any(len(value) > 120 for value in values):
        raise MetricError("metric label value exceeds 120 characters")
    return values


def _guard_series(
    descriptor: MetricDescriptor,
    values: dict[LabelValues, object],
    key: LabelValues,
) -> None:
    if key not in values and len(values) >= descriptor.max_series:
        raise MetricError(f"metric {descriptor.name} exceeded its series budget")


def _escape_help(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n")


def _escape_label(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("\n", "\\n")
        .replace('"', '\\"')
    )


def _format_labels(
    names: tuple[str, ...],
    values: LabelValues,
    *,
    extra: tuple[str, str] | None = None,
) -> str:
    pairs = [f'{name}="{_escape_label(value)}"' for name, value in zip(names, values)]
    if extra is not None:
        pairs.append(f'{extra[0]}="{_escape_label(extra[1])}"')
    return "{" + ",".join(pairs) + "}" if pairs else ""


def _number(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return repr(value)
