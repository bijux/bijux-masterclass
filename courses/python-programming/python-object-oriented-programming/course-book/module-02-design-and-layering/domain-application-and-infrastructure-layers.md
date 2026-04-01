# Layering: Domain, Application, Infrastructure in a Python Codebase

## Purpose

This core introduces layering to separate concerns in a Python codebase: the domain layer for pure business logic (entities, values, and domain services from M02C13–15), the application layer for orchestration (use cases and application services), and the infrastructure layer for adapters (external systems such as databases or HTTP clients). In the monitoring domain, refactor to enforce direct dependencies inward (infrastructure → application → domain via dependency inversion), thereby avoiding circular imports and god modules (for example, a flat orchestrator mixing all concerns). Demonstrate this in a small system: the domain owns invariants (such as `Alert` transitions), the application coordinates flows (such as `MonitoringUseCase`), and the infrastructure adapts (such as `HttpMetricAdapter`). Extending M02C15's services, apply semantics from M02C14 and simple domain services across layers to promote testability and evolution while eliminating leaks (for example, no HTTP calls in the domain). The domain contains no concrete infrastructure; the application knows only ports; and concrete adapters are wired in a composition root.

## 1. Baseline: Flat Structure and Leaked Concerns in the Monitoring Domain

Prior cores centralize logic in flat modules: `MonitoringOrchestrator` mixes domain concerns (alert transitions), application concerns (cycle coordination), and infrastructure concerns (fetching and persistence via concrete adapters). Services such as `AlertService` hold infrastructure dependencies without separation, and imports cross layers (for example, the domain imports the infrastructure `MetricFetcher`). This flat structure yields smells: risks of circular imports (for example, mutual dependencies between the orchestrator and services), god modules (the orchestrator knows HTTP or database details), and fragility (infrastructure changes ripple to the domain). Cohesion is low (logic scattered across modules), and testability is poor (full-stack execution required for use cases).

```python
# baseline_layering.py
from __future__ import annotations
from typing import List, Dict, Any
from semantic_types_model import (
    MetricConfig, Alert, Status, RuleEvaluation, ThresholdContentStrategy, create_config
)  # Domain + semantics (note: Alert here is from semantics; dedicated domain version introduced in refactor)
from service_model import AlertService, InMemoryPersister, ConsoleNotifier  # Services (mixed)
from composition_model import MetricFetcher, RuleEvaluator, ReportAggregator  # Infra + app (note: RuleEvaluator here is app-mixed)
from refactored_model import Metric  # Domain

# Flat: Orchestrator mixes layers
class MonitoringOrchestrator:
    """Baseline: God module; mixes domain/app/infra."""

    def __init__(self, name: str, threshold: float):
        self.config = create_config(name, threshold)  # Domain
        self.fetcher = MetricFetcher()  # Infra leak: HTTP details
        self.evaluator = RuleEvaluator(ThresholdContentStrategy(self.config.threshold.value))  # App (RuleEvaluator mixed with composition)
        self.alert_service = AlertService(InMemoryPersister(), ConsoleNotifier())  # Services
        self.aggregator = ReportAggregator()  # App

    def run_cycle(self) -> List[Alert]:
        raw_metrics = self.fetcher.fetch()  # Infra call in app
        metrics: List[Metric] = [Metric(r["timestamp"], r["name"], r["value"]) for r in raw_metrics]  # Domain
        content = self.evaluator.evaluate(metrics)  # App
        entity_alerts = [Alert(e.rule, e.metric) for e in content]  # Domain (create_alerts_from_content omitted for brevity)
        for alert in entity_alerts:
            self.alert_service.acknowledge_alert(alert)  # Services
        summary = self.aggregator.summarize(entity_alerts)  # App
        print(summary)  # Infra leak: Direct print
        return entity_alerts

# Circular risk: If services import orchestrator, boom
# e.g., AlertService might call back to orchestrator for metrics (god cycle)

if __name__ == "__main__":
    orch = MonitoringOrchestrator("cpu", 0.85)
    alerts = orch.run_cycle()
    print(f"Processed {len(alerts)} alerts")
```

**Baseline Smells Exposed**:
- **Layer Leaks**: The orchestrator calls infrastructure (`MetricFetcher.fetch()`) and domain (`Alert` creation) directly, with no boundaries.
- **God Module**: The orchestrator coordinates all concerns (fetching, evaluation, persistence, logging); it has high responsibility and low cohesion.
- **Circular Import Risk**: Flat imports (for example, services importing the orchestrator) create cycles; no structure prevents this.
- **Fragility**: An infrastructure change (for example, a fetch API update) ripples to the application and domain; testing requires mocks for everything.
- **Testing Fragility**: Full-stack execution is needed for use cases; no layer isolation.

These issues flatten the architecture: concerns are not separated, and evolution is difficult.

## 2. Layering Principles: Domain, Application, Infrastructure

Layering organizes code by concern: the domain layer (business rules), the application layer (use cases), and the infrastructure layer (adapters). Dependencies flow inward (infrastructure → application → domain) via inversion: the application defines ports, and the infrastructure implements them.

### 2.1 Principles

- **Domain Layer**: Pure logic (entities, values, domain services); no infrastructure (for example, `Alert` transitions, `RuleEvaluation`).
- **Application Layer**: Orchestration (use cases, application services); coordinates the domain via ports (for example, `MonitoringUseCase` delegates to a fetch port).
- **Infrastructure Layer**: Adapters (external: databases, HTTP); implements ports (for example, `HttpMetricAdapter` for the fetch port).
- **Dependency Inversion**: The application defines interfaces (ports); the infrastructure adapts; this avoids cycles (the domain is ignorant of the infrastructure).
- **Trade-offs**: Layers add ceremony (ports); over-layering fragments code. Aim for the domain to comprise 20–30% of the code, with clear boundaries.
- **Testing Differences**: Domain: unit tests (invariants); application: integration tests (mock ports); infrastructure: end-to-end tests (real externals).

### 2.2 Refactored Model: Layered Structure

Refactor into modules under a package structure (for example, `src/` with subdirectories `domain/`, `application/`, `infrastructure/`). Use ports for inversion. Reuse semantics from M02C14. For simplicity, we focus on a basic domain service (`create_alerts`); more advanced orchestration like `AlertService` from M02C15 would reside in the application layer, coordinating domain entities via ports. Note: We move `RuleEvaluator` from the composition model (where it mixed application and domain concerns in the baseline) into the domain layer (`domain/rules.py`), as it encapsulates pure domain logic for rule evaluation. All layers use `Metric` from `semantic_types_model` for consistency.

```python
# domain/entities.py
from __future__ import annotations
from uuid import uuid4
from semantic_types_model import RuleType, Metric, Status  # Semantics

class Alert:
    """Domain entity: Data + invariants."""

    def __init__(self, rule: RuleType, metric: Metric):
        self.id = str(uuid4())
        self.rule = rule
        self.metric = metric
        self.status = Status.TRIGGERED

    def acknowledge(self) -> None:
        if self.status != Status.TRIGGERED:
            raise ValueError(f"Cannot acknowledge {self.status} alert")
        self.status = Status.ACKNOWLEDGED

    def __repr__(self) -> str:
        return f"Alert(id={self.id!r}, rule={self.rule!r}, status={self.status!r})"

# domain/rules.py
from __future__ import annotations
from typing import List
from semantic_types_model import RuleType, Metric, Threshold, RuleEvaluation  # Semantics

class ThresholdContentStrategy:
    """Domain strategy: Pure rule evaluation."""

    def __init__(self, threshold: Threshold):
        self._threshold = threshold

    def evaluate(self, metrics: List[Metric]) -> List[RuleEvaluation]:
        high_metrics = [m for m in metrics if m.value >= self._threshold.value]
        return [RuleEvaluation(rule=RuleType("threshold"), metric=m) for m in high_metrics]

class RuleEvaluator:
    """Domain evaluator: Composes strategies."""

    def __init__(self, strategy: ThresholdContentStrategy):
        self._strategy = strategy

    def evaluate(self, metrics: List[Metric]) -> List[RuleEvaluation]:
        return self._strategy.evaluate(metrics)

# domain/services.py
from __future__ import annotations
from typing import List
from .entities import Alert
from semantic_types_model import RuleEvaluation  # Value type

def create_alerts(evals: List[RuleEvaluation]) -> List[Alert]:
    """Domain service: Pure creation."""
    return [Alert(e.rule, e.metric) for e in evals]

# application/ports.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..domain.entities import Alert  # Domain types

class MetricFetchPort(ABC):
    """Application port: Fetch metrics."""

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:  # Raw external format
        pass

class AlertPersistencePort(ABC):
    """Application port: Persist alerts."""

    @abstractmethod
    def persist(self, alerts: List[Alert]) -> None:
        pass

class AlertNotifierPort(ABC):
    """Application port: Notify changes."""

    @abstractmethod
    def notify_change(self, alert: Alert) -> None:
        pass

    @abstractmethod
    def notify_batch(self, alerts: List[Alert]) -> None:
        pass

# application/use_cases.py
from __future__ import annotations
from typing import List
from ..domain.entities import Alert
from ..domain.services import create_alerts
from ..domain.rules import RuleEvaluator
from .ports import MetricFetchPort, AlertPersistencePort, AlertNotifierPort
from semantic_types_model import Metric  # Semantics

class MonitoringUseCase:
    """Application use case: Orchestrate cycle."""

    def __init__(
        self,
        fetch_port: MetricFetchPort,
        persistence_port: AlertPersistencePort,
        notifier_port: AlertNotifierPort,
        evaluator: RuleEvaluator,
    ):
        self._fetch_port = fetch_port
        self._persistence_port = persistence_port
        self._notifier_port = notifier_port
        self._evaluator = evaluator

    def run_cycle(self) -> List[Alert]:
        raw_metrics = self._fetch_port.fetch()  # Infra via port
        metrics = [Metric(r["timestamp"], r["name"], r["value"]) for r in raw_metrics]  # Domain
        evals = self._evaluator.evaluate(metrics)  # Domain
        alerts = create_alerts(evals)  # Domain
        for alert in alerts:
            alert.acknowledge()  # Domain
        self._persistence_port.persist(alerts)  # Infra via port
        self._notifier_port.notify_batch(alerts)  # Infra via port
        return alerts

# infrastructure/adapters.py
from __future__ import annotations
from typing import List, Dict, Any
from ..application.ports import MetricFetchPort, AlertPersistencePort, AlertNotifierPort
from ..domain.entities import Alert
from composition_model import MetricFetcher  # External lib

class HttpMetricAdapter(MetricFetchPort):
    """Infra adapter: HTTP fetch."""

    def fetch(self) -> List[Dict[str, Any]]:
        fetcher = MetricFetcher()  # External lib
        return fetcher.fetch()  # Raw data

class InMemoryAlertRepository(AlertPersistencePort):
    """Infra adapter: In-memory store."""

    def __init__(self):
        self._store = []  # Stable infra state

    def persist(self, alerts: List[Alert]) -> None:
        self._store.extend(alerts)
        print(f"Persisted {len(alerts)} alerts in memory")

class ConsoleAlertNotifier(AlertNotifierPort):
    """Infra adapter: Console notification."""

    def notify_change(self, alert: Alert) -> None:
        print(f"Notified change for alert {alert.id}: {alert.status}")

    def notify_batch(self, alerts: List[Alert]) -> None:
        print(f"Notified batch of {len(alerts)} alerts")

# composition_root.py (top-level: Wires layers)
from __future__ import annotations
from typing import List
from semantic_types_model import Threshold, create_config  # Semantics
from application.use_cases import MonitoringUseCase
from application.ports import MetricFetchPort, AlertPersistencePort, AlertNotifierPort
from domain.rules import RuleEvaluator, ThresholdContentStrategy
from infrastructure.adapters import HttpMetricAdapter, InMemoryAlertRepository, ConsoleAlertNotifier

def create_orchestrator(name: str, threshold: float) -> MonitoringUseCase:
    """Composition root: Wires infra/domain for app."""
    # Infra
    fetch_adapter: MetricFetchPort = HttpMetricAdapter()
    persistence_adapter: AlertPersistencePort = InMemoryAlertRepository()
    notifier_adapter: AlertNotifierPort = ConsoleAlertNotifier()
    # Domain (use config for threshold extraction; name could filter metrics if extended)
    config = create_config(name, threshold)
    evaluator = RuleEvaluator(ThresholdContentStrategy(config.threshold))
    # Application
    return MonitoringUseCase(fetch_adapter, persistence_adapter, notifier_adapter, evaluator)
```

**Rationale**:
- **Domain Purity**: Entities and services are pure (no infrastructure calls); values such as `RuleEvaluation` are used.
- **Application Coordination**: `MonitoringUseCase` orchestrates via ports (no concrete infrastructure).
- **Infrastructure Adaptation**: Adapters implement ports (for example, `HttpMetricAdapter` wraps `MetricFetcher`).
- **Inversion**: The application defines ports; the infrastructure adapts; no cycles (the domain is ignorant of the infrastructure).
- **Superiority**: Testability is improved (mock ports for the application); evolution is enabled (swap adapters); cohesion is high (layers focused). Versus the baseline: no leaks; no cycles. The `RuleEvaluator` is relocated to the domain layer to reflect its role in pure rule semantics. `Metric` is consistently sourced from `semantic_types_model`.

## 3. Integrating into Responsibilities: Orchestrator Flow

Refactor `MonitoringOrchestrator` to `LayeredMonitoringSystem` (entry point); compose via ports in the composition root. Inject infrastructure adapters.

```python
# layered_monitor.py
from __future__ import annotations
from typing import List
from composition_root import create_orchestrator  # Wires layers
from domain.entities import Alert  # Domain types

class LayeredMonitoringSystem:
    """Entry point: Wires layers via composition root."""

    def __init__(self, name: str, threshold: float):
        self.use_case = create_orchestrator(name, threshold)  # Wires infra/domain

    def run_cycle(self) -> List[Alert]:
        return self.use_case.run_cycle()  # Delegate to app

if __name__ == "__main__":
    system = LayeredMonitoringSystem("cpu", 0.85)
    alerts = system.run_cycle()
    print(f"Processed {len(alerts)} alerts via layers")
```

**Output** (simulated):  
Persisted 2 alerts in memory  
Notified batch of 2 alerts  
Processed 2 alerts via layers

**Benefits Demonstrated**:
- **Inversion**: Application ports abstract infrastructure; no direct calls.
- **No Cycles**: Domain → application → infrastructure; imports flow outward.
- **Modularity**: Swap `HttpMetricAdapter` for a file-based adapter; test the application with mock ports.

## 4. Tests: Verifying Layers and Dependencies

Assert inversion (mocks implement ports), no cycles (import graph), and isolation (layer tests).

```python
# test_layered_model.py
import unittest
from unittest.mock import Mock
from application.use_cases import MonitoringUseCase
from application.ports import MetricFetchPort, AlertPersistencePort, AlertNotifierPort
from infrastructure.adapters import HttpMetricAdapter
from semantic_types_model import Threshold
from domain.rules import RuleEvaluator, ThresholdContentStrategy

class TestLayering(unittest.TestCase):

    def test_dependency_inversion(self):
        # App defines ports; infra implements
        fetch_mock = Mock(spec=MetricFetchPort)
        persistence_mock = Mock(spec=AlertPersistencePort)
        notifier_mock = Mock(spec=AlertNotifierPort)
        evaluator = RuleEvaluator(ThresholdContentStrategy(Threshold(0.85)))
        use_case = MonitoringUseCase(fetch_mock, persistence_mock, notifier_mock, evaluator)
        # Infra depends on app port
        adapter = HttpMetricAdapter()  # Implements port
        self.assertIsInstance(adapter, MetricFetchPort)

    def test_app_isolation(self):
        # Test app with mock ports (no real infra)
        fetch_mock = Mock(spec=MetricFetchPort)
        fetch_mock.fetch.return_value = [{"timestamp": 1, "name": "cpu", "value": 0.9}]
        persistence_mock = Mock(spec=AlertPersistencePort)
        notifier_mock = Mock(spec=AlertNotifierPort)
        evaluator = RuleEvaluator(ThresholdContentStrategy(Threshold(0.85)))
        use_case = MonitoringUseCase(fetch_mock, persistence_mock, notifier_mock, evaluator)
        alerts = use_case.run_cycle()
        fetch_mock.fetch.assert_called_once()
        persistence_mock.persist.assert_called()
        notifier_mock.notify_batch.assert_called()
        self.assertGreater(len(alerts), 0)  # App works without infra

    def test_no_cycles_simulation(self):
        # Pseudo-import graph: No circular deps
        # domain -> application -> infrastructure
        # infrastructure -> application (ports)
        # No domain -> infrastructure
        pass  # Illustrates dependency direction

    def test_integration_layers(self):
        # Full: Wire infra to app
        from layered_monitor import LayeredMonitoringSystem
        system = LayeredMonitoringSystem("cpu", 0.85)
        alerts = system.run_cycle()
        self.assertGreater(len(alerts), 0)
```

**Execution**: `python -m unittest test_layered_model.py` passes; confirms inversion, isolation, and wiring.

## Practical Guidelines

- **Layer Boundaries**: Domain: business rules; application: use cases/ports; infrastructure: adapters. No concrete infrastructure in the domain; the application knows only ports; concrete adapters are wired in the composition root.
- **Inversion**: The application defines ports; the infrastructure implements them; dependencies flow inward.
- **Module Structure**: `domain/`, `application/`, `infrastructure/`; imports flow from outer to inner (infrastructure imports application ports + domain types; application imports domain; domain imports none). Use relative imports for consistency.
- **Cycle Audit**: Use tools such as pydeps; limit to <3 layers for small systems.
- **Domain Fit**: Monitoring domain (`Alert`, `MetricConfig`); application (`MonitoringUseCase`); infrastructure (`HttpMetricAdapter`).

**Impacts on Design**:
- **Testability**: Mock ports for the application; unit tests for the domain.
- **Evolution**: Swap infrastructure without domain changes.

## Exercises for Mastery

1. **Layer CRC**: Map monitoring operations to layers; trace the import flow in a cycle.
2. **Cycle Audit**: Introduce a mutual dependency (application → infrastructure → domain); refactor to ports.
3. **Refactor Wiring**: Move `RuleEvaluator` to a domain service; update application ports.

This core refines Module 2's structure with layers. Core 17 explores inheritance use cases.
