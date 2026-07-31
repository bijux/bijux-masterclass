from __future__ import annotations

from dataclasses import dataclass

from .composition import FieldWrapper, NormalizeText, OneOf, describe_layers
from .external import CountingStore, ExternalField


@dataclass(frozen=True, slots=True)
class ColumnContract:
    name: str
    layers: tuple[str, ...]
    backend_owner: str
    source_of_truth: str

    def manifest(self) -> dict[str, object]:
        return {
            "name": self.name,
            "layers": list(self.layers),
            "backend_owner": self.backend_owner,
            "source_of_truth": self.source_of_truth,
        }


def build_incident_model(store: CountingStore) -> type[object]:
    """Build one isolated model class around an explicitly supplied backend."""

    class Incident:
        severity = NormalizeText(
            OneOf(
                ExternalField(store, namespace="incident-model"),
                choices=("info", "warning", "critical"),
            )
        )
        summary = ExternalField(store, namespace="incident-model")

        def __init__(
            self,
            record_id: int,
            *,
            severity: object | None = None,
            summary: object | None = None,
        ) -> None:
            self.record_id = record_id
            if severity is not None:
                self.severity = severity
            if summary is not None:
                self.summary = summary

    Incident.__name__ = "Incident"
    return Incident


def inspect_columns(model: type[object]) -> list[ColumnContract]:
    columns: list[ColumnContract] = []
    for name, declared in vars(model).items():
        current = declared
        while isinstance(current, FieldWrapper):
            current = current.inner
        if not isinstance(current, ExternalField):
            continue
        layers = tuple(layer["type"] for layer in describe_layers(declared))
        columns.append(
            ColumnContract(
                name=name,
                layers=layers,
                backend_owner=type(current.store).__name__,
                source_of_truth="backend JSON slot",
            )
        )
    return columns


def relational_model_evidence() -> dict[str, object]:
    store = CountingStore()
    incident_type = build_incident_model(store)
    incident = incident_type(
        41,
        severity=" WARNING ",
        summary="queue depth exceeded",
    )
    observer = incident_type(41)

    loaded = {
        "severity": observer.severity,
        "summary": observer.summary,
    }

    writes_before_rejection = len(
        [event for event in store.events if event["operation"] == "write"]
    )
    try:
        incident_type(42, severity="urgent", summary="unsupported severity")
    except ValueError as error:
        rejection = str(error)
    else:
        raise AssertionError("unsupported severity was unexpectedly accepted")
    writes_after_rejection = len(
        [event for event in store.events if event["operation"] == "write"]
    )

    return {
        "columns": [column.manifest() for column in inspect_columns(incident_type)],
        "loaded_from_second_instance": loaded,
        "backend_events": store.events,
        "rejected_write": {
            "error": rejection,
            "backend_writes_added": writes_after_rejection - writes_before_rejection,
        },
        "field_layer_owns": [
            "one stable backend key per attribute",
            "JSON scalar serialization",
            "severity normalization and choice validation",
            "local read-through cache",
        ],
        "explicitly_absent": [
            "transactions",
            "identity map",
            "query planning",
            "relationship loading",
            "schema migration",
        ],
        "production_orm": False,
    }
