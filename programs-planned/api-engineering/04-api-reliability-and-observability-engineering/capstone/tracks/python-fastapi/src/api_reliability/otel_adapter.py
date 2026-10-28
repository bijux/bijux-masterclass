"""Optional OpenTelemetry SDK adapter.

The dependency-light proof does not import this module. The full environment
installs the pinned OpenTelemetry packages and exercises this adapter against an
OpenTelemetry Collector. Keeping the adapter separate prevents a missing SDK
from being misreported as a passing reliability proof.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OTelSettings:
    service_name: str
    service_version: str
    environment: str
    otlp_endpoint: str
    trace_sample_ratio: float = 0.1


def configure(settings: OTelSettings) -> object:
    try:
        from opentelemetry import metrics, trace
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.metrics import MeterProvider
        from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased
    except ImportError as error:
        raise RuntimeError("install the pinned OpenTelemetry environment") from error

    if not 0 <= settings.trace_sample_ratio <= 1:
        raise ValueError("trace_sample_ratio must be between zero and one")
    resource = Resource.create(
        {
            "service.name": settings.service_name,
            "service.version": settings.service_version,
            "deployment.environment.name": settings.environment,
        }
    )
    tracer_provider = TracerProvider(
        resource=resource,
        sampler=ParentBased(TraceIdRatioBased(settings.trace_sample_ratio)),
    )
    tracer_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{settings.otlp_endpoint}/v1/traces"))
    )
    trace.set_tracer_provider(tracer_provider)

    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=f"{settings.otlp_endpoint}/v1/metrics")
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)
    return {"tracer_provider": tracer_provider, "meter_provider": meter_provider}
