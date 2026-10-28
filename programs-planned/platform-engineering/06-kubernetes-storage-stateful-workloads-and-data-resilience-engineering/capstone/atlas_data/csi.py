from __future__ import annotations

from dataclasses import dataclass, field
import hashlib


class CSIError(RuntimeError):
    pass


@dataclass
class VolumeState:
    id: str
    name: str
    capacity_gib: int
    zone: str
    attached_nodes: set[str] = field(default_factory=set)
    staged_nodes: set[str] = field(default_factory=set)
    published_targets: set[str] = field(default_factory=set)
    deleted: bool = False


class SemanticCSI:
    def __init__(self, driver_name: str):
        self.driver_name = driver_name
        self._by_id: dict[str, VolumeState] = {}
        self._by_name: dict[str, str] = {}
        self.ledger: list[dict[str, str]] = []

    def _record(self, operation: str, volume_id: str, result: str) -> None:
        self.ledger.append({"operation": operation, "volumeId": volume_id, "result": result})

    def create_volume(self, name: str, capacity_gib: int, zone: str) -> VolumeState:
        if capacity_gib <= 0:
            raise CSIError("capacity must be positive")
        existing_id = self._by_name.get(name)
        if existing_id:
            existing = self._by_id[existing_id]
            if existing.capacity_gib != capacity_gib or existing.zone != zone:
                raise CSIError("create request conflicts with existing volume")
            self._record("CreateVolume", existing.id, "replayed")
            return existing
        digest = hashlib.sha256(f"{self.driver_name}:{name}".encode()).hexdigest()[:16]
        volume = VolumeState(digest, name, capacity_gib, zone)
        self._by_id[volume.id] = volume
        self._by_name[name] = volume.id
        self._record("CreateVolume", volume.id, "created")
        return volume

    def volume(self, volume_id: str) -> VolumeState:
        try:
            volume = self._by_id[volume_id]
        except KeyError as exc:
            raise CSIError("volume not found") from exc
        if volume.deleted:
            raise CSIError("volume is deleted")
        return volume

    def controller_publish(self, volume_id: str, node_id: str) -> None:
        volume = self.volume(volume_id)
        if volume.attached_nodes and node_id not in volume.attached_nodes:
            raise CSIError("multi-attach prohibited")
        result = "replayed" if node_id in volume.attached_nodes else "attached"
        volume.attached_nodes.add(node_id)
        self._record("ControllerPublishVolume", volume_id, result)

    def node_stage(self, volume_id: str, node_id: str) -> None:
        volume = self.volume(volume_id)
        if node_id not in volume.attached_nodes:
            raise CSIError("volume is not attached to node")
        result = "replayed" if node_id in volume.staged_nodes else "staged"
        volume.staged_nodes.add(node_id)
        self._record("NodeStageVolume", volume_id, result)

    def node_publish(self, volume_id: str, node_id: str, target: str) -> None:
        volume = self.volume(volume_id)
        if node_id not in volume.staged_nodes:
            raise CSIError("volume is not staged on node")
        result = "replayed" if target in volume.published_targets else "published"
        volume.published_targets.add(target)
        self._record("NodePublishVolume", volume_id, result)

    def node_unpublish(self, volume_id: str, target: str) -> None:
        volume = self.volume(volume_id)
        volume.published_targets.discard(target)
        self._record("NodeUnpublishVolume", volume_id, "unpublished")

    def node_unstage(self, volume_id: str, node_id: str) -> None:
        volume = self.volume(volume_id)
        if volume.published_targets:
            raise CSIError("published targets remain")
        volume.staged_nodes.discard(node_id)
        self._record("NodeUnstageVolume", volume_id, "unstaged")

    def controller_unpublish(self, volume_id: str, node_id: str) -> None:
        volume = self.volume(volume_id)
        if node_id in volume.staged_nodes:
            raise CSIError("volume remains staged")
        volume.attached_nodes.discard(node_id)
        self._record("ControllerUnpublishVolume", volume_id, "detached")

    def expand(self, volume_id: str, new_capacity_gib: int) -> None:
        volume = self.volume(volume_id)
        if new_capacity_gib < volume.capacity_gib:
            raise CSIError("volume shrink is unsupported")
        result = "replayed" if new_capacity_gib == volume.capacity_gib else "expanded"
        volume.capacity_gib = new_capacity_gib
        self._record("ControllerExpandVolume", volume_id, result)

    def delete_volume(self, volume_id: str) -> None:
        volume = self.volume(volume_id)
        if volume.attached_nodes or volume.staged_nodes or volume.published_targets:
            raise CSIError("volume is still in use")
        volume.deleted = True
        self._record("DeleteVolume", volume_id, "deleted")
