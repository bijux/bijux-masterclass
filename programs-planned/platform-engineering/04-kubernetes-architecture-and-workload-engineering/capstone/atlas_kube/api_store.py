from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable
import copy

from .models import KubeObject, now_rfc3339


class ApiError(RuntimeError):
    pass


class NotFound(ApiError):
    pass


class AlreadyExists(ApiError):
    pass


class VersionConflict(ApiError):
    pass


class ApplyConflict(ApiError):
    def __init__(self, paths: list[str]):
        self.paths = sorted(paths)
        super().__init__("apply conflict on: " + ", ".join(self.paths))


@dataclass(slots=True)
class WriteRecord:
    action: str
    key: tuple[str, str, str, str]
    resource_version: int
    manager: str


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    """Flatten dictionaries to field paths; lists are atomic for this course model."""
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            result.update(_flatten(child, path))
        return result
    return {prefix: copy.deepcopy(value)}


def _set_path(target: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    cursor = target
    for part in parts[:-1]:
        next_value = cursor.get(part)
        if not isinstance(next_value, dict):
            next_value = {}
            cursor[part] = next_value
        cursor = next_value
    cursor[parts[-1]] = copy.deepcopy(value)


class ApiStore:
    """A deterministic model of API persistence, concurrency, apply, and deletion."""

    def __init__(self) -> None:
        self._objects: dict[tuple[str, str, str, str], KubeObject] = {}
        self._revision = 0
        self.writes: list[WriteRecord] = []

    @property
    def revision(self) -> int:
        return self._revision

    def _commit(self, obj: KubeObject, action: str, manager: str) -> KubeObject:
        self._revision += 1
        obj.metadata.resource_version = self._revision
        self._objects[obj.key] = obj.clone()
        self.writes.append(WriteRecord(action, obj.key, self._revision, manager))
        return obj.clone()

    def create(self, obj: KubeObject, manager: str = "client") -> KubeObject:
        if obj.key in self._objects:
            raise AlreadyExists(str(obj.key))
        created = obj.clone()
        created.metadata.resource_version = 0
        return self._commit(created, "create", manager)

    def get(self, api_version: str, kind: str, namespace: str, name: str) -> KubeObject:
        key = (api_version, kind, namespace, name)
        try:
            return self._objects[key].clone()
        except KeyError as exc:
            raise NotFound(str(key)) from exc

    def maybe_get(self, api_version: str, kind: str, namespace: str, name: str) -> KubeObject | None:
        try:
            return self.get(api_version, kind, namespace, name)
        except NotFound:
            return None

    def list(self, *, api_version: str | None = None, kind: str | None = None,
             namespace: str | None = None, labels: dict[str, str] | None = None) -> list[KubeObject]:
        result = []
        for obj in self._objects.values():
            if api_version is not None and obj.api_version != api_version:
                continue
            if kind is not None and obj.kind != kind:
                continue
            if namespace is not None and obj.metadata.namespace != namespace:
                continue
            if labels and any(obj.metadata.labels.get(k) != v for k, v in labels.items()):
                continue
            result.append(obj.clone())
        return sorted(result, key=lambda o: (o.kind, o.metadata.namespace, o.metadata.name))

    def replace(self, obj: KubeObject, expected_resource_version: int,
                manager: str = "client", *, status_only: bool = False) -> KubeObject:
        current = self.get(*obj.key)
        if current.metadata.resource_version != expected_resource_version:
            raise VersionConflict(
                f"expected {expected_resource_version}, current {current.metadata.resource_version}"
            )
        updated = obj.clone()
        updated.metadata.uid = current.metadata.uid
        if not status_only and updated.spec != current.spec:
            updated.metadata.generation = current.metadata.generation + 1
        else:
            updated.metadata.generation = current.metadata.generation
        return self._commit(updated, "status" if status_only else "replace", manager)

    def update_status(self, obj: KubeObject, status: dict[str, Any],
                      manager: str = "controller") -> KubeObject:
        current = self.get(*obj.key)
        if current.status == status:
            return current
        current.status = copy.deepcopy(status)
        return self._commit(current, "status", manager)

    def apply(self, api_version: str, kind: str, namespace: str, name: str,
              patch: dict[str, Any], manager: str, *, force: bool = False) -> KubeObject:
        current = self.get(api_version, kind, namespace, name)
        fields = _flatten(patch)
        conflicts: list[str] = []
        for path in fields:
            for other, owned in current.metadata.managed_fields.items():
                if other != manager and path in owned:
                    conflicts.append(path)
        if conflicts and not force:
            raise ApplyConflict(conflicts)
        if force:
            for owned in current.metadata.managed_fields.values():
                owned.difference_update(fields)
        old_spec = copy.deepcopy(current.spec)
        root = {"spec": current.spec, "metadata": {"labels": current.metadata.labels,
                                                   "annotations": current.metadata.annotations}}
        for path, value in fields.items():
            _set_path(root, path, value)
        current.spec = root["spec"]
        current.metadata.labels = root["metadata"]["labels"]
        current.metadata.annotations = root["metadata"]["annotations"]
        current.metadata.managed_fields.setdefault(manager, set()).update(fields)
        if current.spec != old_spec:
            current.metadata.generation += 1
        return self._commit(current, "apply-force" if force else "apply", manager)

    def add_finalizer(self, obj: KubeObject, finalizer: str, manager: str) -> KubeObject:
        current = self.get(*obj.key)
        if finalizer in current.metadata.finalizers:
            return current
        current.metadata.finalizers.append(finalizer)
        return self._commit(current, "add-finalizer", manager)

    def remove_finalizer(self, obj: KubeObject, finalizer: str, manager: str) -> KubeObject | None:
        current = self.get(*obj.key)
        if finalizer not in current.metadata.finalizers:
            return current
        current.metadata.finalizers.remove(finalizer)
        committed = self._commit(current, "remove-finalizer", manager)
        if committed.metadata.deletion_timestamp and not committed.metadata.finalizers:
            self._objects.pop(committed.key, None)
            self._revision += 1
            self.writes.append(WriteRecord("delete-complete", committed.key, self._revision, manager))
            return None
        return committed

    def delete(self, obj: KubeObject, manager: str = "client") -> KubeObject | None:
        current = self.get(*obj.key)
        if current.metadata.finalizers:
            if current.metadata.deletion_timestamp is None:
                current.metadata.deletion_timestamp = now_rfc3339()
                return self._commit(current, "delete-pending", manager)
            return current
        self._objects.pop(current.key, None)
        self._revision += 1
        self.writes.append(WriteRecord("delete", current.key, self._revision, manager))
        return None

    def delete_owned_by(self, owner_uid: str, manager: str = "garbage-collector") -> int:
        victims = [obj for obj in self._objects.values()
                   if any(ref.get("uid") == owner_uid for ref in obj.metadata.owner_references)]
        for obj in victims:
            self.delete(obj, manager)
        return len(victims)

    def watch_since(self, resource_version: int) -> list[WriteRecord]:
        return [record for record in self.writes if record.resource_version > resource_version]
