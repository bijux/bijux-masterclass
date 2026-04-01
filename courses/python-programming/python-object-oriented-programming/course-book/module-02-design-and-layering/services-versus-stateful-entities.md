# Service Objects and Operations vs Stateful Entities

## Purpose

This core distinguishes stateful entities—data carriers with identity and domain behavior (e.g., `Alert`, `MetricConfig` from M02C13/14)—from service objects, which encapsulate orchestration and cross-cutting operations without owning the domain model (e.g., `RuleEvaluator`, `AlertService`). In the monitoring domain, extract coordination (e.g., persistence, notifications) into services to promote cohesion, testability, and reusability, avoiding bloated entities (data + infrastructure mixing) or god objects (orchestrators handling all concerns). Demonstrate when services form real abstractions (e.g., pluggable `AlertService` for lifecycle coordination) versus dumping grounds (e.g., procedural functions). Extending M02C14's semantics, refactor to compose services with semantic types, reducing entity bloat and enhancing modularity. Entities retain domain logic (e.g., transition invariants); services hold stable collaborators (e.g., ports) and delegate external concerns. Note: This core relocates and finalizes the `Alert` entity definition, superseding prior versions.

## 1. Baseline: Blurred Responsibilities in the Monitoring Domain

Prior cores embed operations into entities or centralize in orchestrators: `Alert.acknowledge` mixes domain logic with infrastructure (e.g., persistence/notification; smell: SRP violation, high responsibility). `MonitoringOrchestrator.run_cycle` handles fetching, evaluation, mutation, persistence, and logging (god-object smell: high responsibility, low cohesion). Ops leak across boundaries. This blurs roles: entities accumulate side effects (tight to infrastructure), orchestrators become procedural (no abstraction). Smells: Coupling (orchestrator knows internals), poor testability (full flow for ops), fragility (changes ripple).

```python
# baseline_services.py
from __future__ import annotations
from typing import List
from uuid import uuid4
from semantic_types_model import Status, RuleType, Metric, create_config, ThresholdContentStrategy, create_alerts_from_content  # From M02C14
from composition_model import MetricFetcher, RuleEvaluator, PersistenceService, ReportAggregator

class Alert:
    """Baseline: Stateful entity with mixed ops (SRP violation)."""

    def __init__(self, rule: RuleType, metric: Metric):
        self.id = str(uuid4())
        self.rule = rule
        self.metric = metric
        self.status = Status.TRIGGERED

    def acknowledge(self, persister: PersistenceService) -> None:  # Embedded infrastructure
        if self.status != Status.TRIGGERED:
            raise ValueError(f"Cannot acknowledge {self.status} alert")
        self.status = Status.ACKNOWLEDGED
        persister.persist([self])  # Leaks persistence
        self.notify_change()  # Side effect

    def notify_change(self) -> None:  # Procedural dump
        print(f"Alert {self.id} status changed to {self.status}")

class MonitoringOrchestrator:
    """Baseline: God object; handles all ops."""

    def __init__(self, name: str, threshold: float):
        self.config = create_config(name, threshold)
        self.fetcher = MetricFetcher()
        self.evaluator = RuleEvaluator(ThresholdContentStrategy(self.config.threshold.value))
        self.persister = PersistenceService()

    def run_cycle(self) -> List[Alert]:
        raw_metrics = self.fetcher.fetch()
        metrics: List[Metric] = [Metric(r["timestamp"], r["name"], r["value"]) for r in raw_metrics]
        content = self.evaluator.evaluate(metrics)
        entity_alerts = create_alerts_from_content(content)
        for alert in entity_alerts:
            alert.acknowledge(self.persister)  # Orchestrator passes deps
            self.log_and_notify(alert)  # God-like: Logging + notification
        return entity_alerts

    def log_and_notify(self, alert: Alert) -> None:  # Procedural dump
        print(f"Logged and notified: {alert.id}")

if __name__ == "__main__":
    orch = MonitoringOrchestrator("cpu", 0.85)
    alerts = orch.run_cycle()
    print(f"Processed {len(alerts)} alerts")
```

**Baseline Smells Exposed**:
- **Entity SRP Violation**: `Alert.acknowledge` mixes domain transition with persistence/notification (infrastructure leak).
- **God Orchestrator**: `run_cycle` coordinates everything (fetch, evaluate, mutate, log); high responsibility, low cohesion, hard to test ops in isolation.
- **Procedural Dumps**: Methods like `log_and_notify` are stateless functions disguised as ops, lacking abstraction (no pluggability).
- **Tight Coupling**: Orchestrator passes deps to entities; changes ripple.
- **Testing Fragility**: Full cycle to test notification; no isolation for ops.

These blur roles: entities leak infrastructure; services vanish into procedures.

## 2. Service Objects vs Stateful Entities: Core Distinctions and Design Principles

Stateful entities hold data with identity and domain behavior (e.g., `Alert`: invariants like valid transitions). Service objects hold stable collaborators (e.g., ports) and orchestrate cross-cutting ops without owning the domain model (e.g., `AlertService`: coordinate persistence/notification).

### 2.1 Principles

- **Stateful Entities**: Data + domain logic (e.g., transition rules); minimal, focused ops; identity/lifecycle primary (from M02C13).
- **Service Objects**: Hold stable collaborators (no domain collections); orchestrate via composition (e.g., `AlertService` delegates to notifier/persister); abstractions for infrastructure/cross-cutting.
- **Distinctions**: Entities mutate self (domain invariants); services act on others (no self-mutation). Avoid bloated entities (SRP violation) or anemic (data-only); services not dumps (procedural).
- **Trade-offs**: Services reduce entity bloat (cohesion); over-extraction fragments. Aim: Entities 1-2 domain ops; services for coordination.
- **Testing Differences**: Entities: Invariants (transitions); services: Input-output (mock collaborators).

### 2.2 Refactored Model: Extracted Services

Refactor: Entities keep domain logic (e.g., `Alert.acknowledge` validates transition); `AlertService` orchestrates external (persist/notify). Use M02C14 semantics.

```python
# service_model.py
from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from uuid import uuid4
from semantic_types_model import Status, RuleType, Metric  # From M02C14

class PersistencePort(ABC):
    """Abstraction: Pluggable persistence."""

    @abstractmethod
    def persist(self, alerts: List['Alert']) -> None:
        pass

class NotifierPort(ABC):
    """Abstraction: Pluggable notification."""

    @abstractmethod
    def notify_change(self, alert: 'Alert') -> None:
        pass

    @abstractmethod
    def notify_batch(self, alerts: List['Alert']) -> None:
        pass

class AlertService:
    """Service: Orchestration for lifecycle (holds stable collaborators)."""

    def __init__(self, persister: PersistencePort, notifier: NotifierPort):
        self._persister = persister
        self._notifier = notifier

    def acknowledge_alert(self, alert: 'Alert') -> None:
        """Orchestrate: Delegate domain transition + external."""
        alert.acknowledge()  # Entity domain logic
        self._persister.persist([alert])
        self._notifier.notify_change(alert)

    def batch_acknowledge(self, alerts: List['Alert']) -> None:
        """Non-trivial: Batch persist, notify summary."""
        for alert in alerts:
            alert.acknowledge()
        self._persister.persist(alerts)  # Batch persist
        self._notifier.notify_batch(alerts)  # Batch notify

class Alert:
    """Stateful entity: Data + domain logic (invariants)."""

    def __init__(self, rule: RuleType, metric: Metric):
        self.id = str(uuid4())
        self.rule = rule
        self.metric = metric
        self.status = Status.TRIGGERED

    def acknowledge(self) -> None:  # Domain op: Invariant only
        if self.status != Status.TRIGGERED:
            raise ValueError(f"Cannot acknowledge {self.status} alert")
        self.status = Status.ACKNOWLEDGED

    def __repr__(self) -> str:
        return f"Alert(id={self.id!r}, rule={self.rule!r}, status={self.status!r})"

# Concrete implementations (pluggable)
class InMemoryPersister(PersistencePort):
    def __init__(self):
        self._store = []  # Stable infra state

    def persist(self, alerts: List[Alert]) -> None:
        self._store.extend(alerts)
        print(f"Persisted {len(alerts)} alerts in memory")

class ConsoleNotifier(NotifierPort):
    def notify_change(self, alert: Alert) -> None:
        print(f"Notified change for alert {alert.id}: {alert.status}")

    def notify_batch(self, alerts: List[Alert]) -> None:
        print(f"Notified batch of {len(alerts)} alerts")

# Example: Lean entities + services
def create_alert(rule: RuleType, metric: Metric) -> Alert:
    return Alert(rule, metric)
```

**Rationale**:
- **Entity Domain Logic**: `Alert.acknowledge` handles invariants (e.g., from triggered only); no infrastructure.
- **Service Orchestration**: `AlertService` coordinates (entity transition + persist + notify); holds stable deps only (no domain collections).
- **Real vs Dumping Ground**: Services abstract concerns (e.g., batching in `batch_acknowledge` with `notify_batch`); not procedural (no hardcoded prints). Vs. baseline: Entities unbloated; ops isolated.
- **Superiority**: Cohesion (entities domain-only); flex (swap notifier/persister). Use M02C14 semantics for fields.

## 3. Integrating into Responsibilities: Orchestrator Flow

Update `MonitoringOrchestrator` (from M02C14) to compose services (e.g., `AlertService` for lifecycle); inject abstractions. Keep entities lean.

```python
# service_monitor.py
from __future__ import annotations
from typing import List
from semantic_types_model import MetricConfig, RuleEvaluation, ThresholdContentStrategy, create_config  # From M02C14
from service_model import AlertService, InMemoryPersister, ConsoleNotifier, Alert, create_alert  # From this core
from composition_model import MetricFetcher, RuleEvaluator, ReportAggregator
from refactored_model import Metric

class MonitoringOrchestrator:
    """Composes services: Delegates ops to abstractions."""

    def __init__(self, name: str, threshold: float):
        self.config = create_config(name, threshold)
        self.fetcher = MetricFetcher()
        self.evaluator = RuleEvaluator(ThresholdContentStrategy(self.config.threshold))
        self.alert_service = AlertService(InMemoryPersister(), ConsoleNotifier())  # Composed service
        self.aggregator = ReportAggregator()

    def run_cycle(self) -> List[Alert]:
        raw_metrics = self.fetcher.fetch()
        metrics: List[Metric] = [Metric(r["timestamp"], r["name"], r["value"]) for r in raw_metrics]
        content = self.evaluator.evaluate(metrics)  # Semantic values
        entity_alerts = [create_alert(e.rule, e.metric) for e in content]  # Lean entities
        self.alert_service.batch_acknowledge(entity_alerts)  # Delegate to service
        return entity_alerts

if __name__ == "__main__":
    orch = MonitoringOrchestrator("cpu", 0.85)
    alerts = orch.run_cycle()
    print(f"Processed {len(alerts)} alerts via services")
```

**Output** (simulated):  
Persisted 2 alerts in memory  
Notified batch of 2 alerts  
Processed 2 alerts via services

**Benefits Demonstrated**:
- **Delegation**: Orchestrator composes services; no god logic.
- **Pluggability**: Swap `InMemoryPersister` for DB; test `AlertService` in isolation.
- **Cohesion**: Entities domain-only; services orchestrate with stable deps.

## 4. Tests: Verifying Services and Isolation

Assert delegation (mock calls), isolation (no entity infrastructure), and invariants.

```python
# test_service_model.py
import unittest
from unittest.mock import Mock
from service_model import AlertService, PersistencePort, NotifierPort, Alert, create_alert
from semantic_types_model import RuleType, Metric, Status  # From M02C14

class TestServices(unittest.TestCase):

    def setUp(self):
        self.persister = Mock(spec=PersistencePort)
        self.notifier = Mock(spec=NotifierPort)
        self.service = AlertService(self.persister, self.notifier)

    def test_service_delegation(self):
        metric = Metric(1, "cpu", 0.9)
        rule = RuleType("threshold")
        alert = create_alert(rule, metric)
        self.service.acknowledge_alert(alert)
        # Delegation: Calls interfaces
        self.persister.persist.assert_called_once_with([alert])
        self.notifier.notify_change.assert_called_once_with(alert)
        # Entity mutated via delegation, invariant held
        self.assertEqual(alert.status, Status.ACKNOWLEDGED)

    def test_batch_orchestration(self):
        metric = Metric(1, "cpu", 0.9)
        rule = RuleType("threshold")
        alerts = [create_alert(rule, metric) for _ in range(2)]
        self.service.batch_acknowledge(alerts)
        # Batch delegation: Single persist call
        self.persister.persist.assert_called_once_with(alerts)
        self.notifier.notify_batch.assert_called_once_with(alerts)
        # Invariants held
        self.assertEqual(alerts[0].status, Status.ACKNOWLEDGED)
        self.assertEqual(alerts[1].status, Status.ACKNOWLEDGED)

    def test_pluggable_abstraction(self):
        # Mock swap: Test isolation
        alert = create_alert(RuleType("threshold"), Metric(1, "cpu", 0.9))
        self.service.acknowledge_alert(alert)
        self.persister.persist.assert_called_once_with([alert])
        self.notifier.notify_change.assert_called_once_with(alert)

    def test_entity_invariant(self):
        metric = Metric(1, "cpu", 0.9)
        rule = RuleType("threshold")
        alert = create_alert(rule, metric)
        alert.status = Status.RESOLVED  # Direct for test
        with self.assertRaises(ValueError):
            alert.acknowledge()  # Invariant: Cannot from resolved

    def test_service_no_domain_aggregates(self):
        # Service holds collaborators only; no domain collections
        self.assertIsNotNone(self.service._persister)
        self.assertIsNotNone(self.service._notifier)
        self.assertFalse(hasattr(self.service, '_alerts'))  # No hidden domain aggregates

    def test_integration_composition(self):
        # Full flow: Orchestrator delegates to service
        from service_monitor import MonitoringOrchestrator
        orch = MonitoringOrchestrator("cpu", 0.85)
        alerts = orch.run_cycle()
        self.assertGreater(len(alerts), 0)

```

**Execution**: `python -m unittest test_service_model.py` passes; confirms delegation, pluggability, and invariants.

## Practical Guidelines

- **Classify Ops**: Entities for data/domain logic (invariants); services for orchestration/external. Ask: "Domain behavior?" → entity; "Coordinates collaborators?" → service.
- **Services with Stable Deps**: Hold collaborators only (no domain collections); input-output determined.
- **Abstraction Check**: Services testable alone (mocks); entities keep invariants.
- **Cohesion Audit**: Entities <3 ops; services focused (1-2 concerns).
- **Domain Fit**: Monitoring entities for alerts/metrics; services for evaluation/persistence.

**Impacts on Design**:
- **Modularity**: Isolated testing; swap implementations (e.g., notifier).
- **Maintainability**: Clear roles; no bloated entities.

## Exercises for Mastery

1. **Service CRC**: Extract `MetricFetcherService` for fetch + validation; trace delegation in cycle.
2. **SRP Audit**: Move `Alert.notify_change` to service; test isolation with mocks.
3. **Refactor Pluggability**: Implement `DBPersister`; swap in orchestrator, assert flow.

This core refines Module 2's roles with services. Core 16 introduces layering.
