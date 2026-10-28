from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Iterable

from .canonical import desired_resource, identity_string, render_digest
from .inventory import Inventory, is_protected
from .models import Drift, ReconcileReport


def _pointer_parts(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError(f"JSON pointer must start with '/': {pointer}")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/") if part]


def _get_pointer(value: dict, pointer: str):
    current = value
    for part in _pointer_parts(pointer):
        if not isinstance(current, dict) or part not in current:
            return None, False
        current = current[part]
    return copy.deepcopy(current), True


def _set_pointer(value: dict, pointer: str, item) -> None:
    parts = _pointer_parts(pointer)
    current = value
    for part in parts[:-1]:
        child = current.get(part)
        if not isinstance(child, dict):
            child = {}
            current[part] = child
        current = child
    if parts:
        current[parts[-1]] = copy.deepcopy(item)


def _preserve_external(desired: dict, live: dict, paths: set[str]) -> dict:
    merged = copy.deepcopy(desired)
    for pointer in sorted(paths):
        item, present = _get_pointer(live, pointer)
        if present:
            _set_pointer(merged, pointer, item)
    return merged


@dataclass
class LiveObject:
    resource: dict
    manager: str
    external_paths: set[str] = field(default_factory=set)


@dataclass
class ClusterState:
    objects: dict[str, LiveObject] = field(default_factory=dict)
    last_source_revision: str | None = None

    def get(self, identity: str) -> dict | None:
        item = self.objects.get(identity)
        return copy.deepcopy(item.resource) if item else None

    def put(self, resource: dict, manager: str = "atlas-gitops", external_paths: set[str] | None = None) -> None:
        self.objects[identity_string(resource)] = LiveObject(copy.deepcopy(resource), manager, external_paths or set())

    def delete(self, identity: str) -> None:
        self.objects.pop(identity, None)


class Reconciler:
    def __init__(self, manager: str = "atlas-gitops") -> None:
        self.manager = manager

    def reconcile(
        self,
        cluster: ClusterState,
        desired: Iterable[dict],
        previous_inventory: Inventory,
        source_revision: str,
        source_available: bool = True,
        suspended: bool = False,
    ) -> tuple[Inventory, ReconcileReport]:
        desired_list = [desired_resource(r) for r in desired]
        report = ReconcileReport(source_revision=source_revision, source_available=source_available)
        if not source_available or suspended:
            return previous_inventory, report

        desired_map = {identity_string(r): r for r in desired_list}
        next_inventory = Inventory(application=previous_inventory.application, identities=set(desired_map))

        for identity, wanted in desired_map.items():
            live = cluster.objects.get(identity)
            if live is None:
                cluster.put(wanted, manager=self.manager)
                report.created.append(identity)
                report.writes += 1
                continue
            current = desired_resource(live.resource)
            effective_wanted = _preserve_external(wanted, current, live.external_paths)
            if current != effective_wanted:
                category = "unauthorized-drift" if live.manager == self.manager else "shared-field-conflict"
                live.resource = copy.deepcopy(effective_wanted)
                live.manager = self.manager
                report.updated.append(identity)
                report.drift.append(Drift(identity, category, "repair-owned-fields", "desired owned fields differ"))
                report.writes += 1
            if live.external_paths:
                report.preserved_external.append(identity)
                report.drift.append(Drift(identity, "externally-managed", "preserve", ",".join(sorted(live.external_paths))))

        for identity in sorted(previous_inventory.identities - set(desired_map)):
            live = cluster.objects.get(identity)
            if live is None:
                continue
            if is_protected(live.resource):
                report.blocked_prune.append(identity)
                report.drift.append(Drift(identity, "protected-prune", "block", "data-owner retirement required"))
                next_inventory.identities.add(identity)
                continue
            cluster.delete(identity)
            report.deleted.append(identity)
            report.writes += 1

        cluster.last_source_revision = source_revision
        return next_inventory, report

    @staticmethod
    def state_digest(cluster: ClusterState) -> str:
        return render_digest(item.resource for item in cluster.objects.values())
