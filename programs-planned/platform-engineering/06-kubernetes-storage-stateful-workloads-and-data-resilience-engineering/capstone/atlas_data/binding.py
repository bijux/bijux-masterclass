from __future__ import annotations

import hashlib
from dataclasses import replace
from .models import BindingResult, Claim, StorageClass, Volume


class BindingError(RuntimeError):
    pass


class Binder:
    def __init__(self, classes: list[StorageClass], volumes: list[Volume] | None = None):
        self.classes = {item.name: item for item in classes}
        self.volumes = {item.name: item for item in (volumes or [])}
        for item in classes:
            item.validate()

    def _matching_volume(self, claim: Claim, zone: str | None) -> Volume | None:
        for volume in self.volumes.values():
            if volume.phase != "Available":
                continue
            if volume.storage_class != claim.storage_class:
                continue
            if volume.capacity_gib < claim.requested_gib:
                continue
            if volume.volume_mode != claim.volume_mode:
                continue
            if not set(claim.access_modes).issubset(set(volume.access_modes)):
                continue
            if zone is not None and volume.zone != zone:
                continue
            return volume
        return None

    def bind(self, claim: Claim, selected_zone: str | None = None) -> BindingResult:
        claim.validate()
        if claim.phase == "Bound":
            volume = self.volumes.get(claim.bound_volume or "")
            if volume is None:
                raise BindingError("bound claim references missing volume")
            return BindingResult(claim, volume, False, ("already-bound",))
        storage_class = self.classes.get(claim.storage_class)
        if storage_class is None:
            raise BindingError("storage class not found")
        if storage_class.binding_mode == "WaitForFirstConsumer" and selected_zone is None:
            raise BindingError("selected topology is required for delayed binding")
        zone = selected_zone or (storage_class.allowed_zones[0] if storage_class.allowed_zones else "any")
        if storage_class.allowed_zones and zone not in storage_class.allowed_zones:
            raise BindingError("selected zone is not allowed by class")
        transitions = ["claim-validated"]
        volume = self._matching_volume(claim, zone)
        created = False
        if volume is None:
            identity = hashlib.sha256(f"{claim.key}:{claim.storage_class}".encode()).hexdigest()[:12]
            name = f"pv-{identity}"
            volume = Volume(
                name=name,
                handle=f"atlas://{zone}/{identity}",
                capacity_gib=claim.requested_gib,
                access_modes=claim.access_modes,
                storage_class=claim.storage_class,
                zone=zone,
                reclaim_policy=storage_class.reclaim_policy,
                volume_mode=claim.volume_mode,
            )
            self.volumes[name] = volume
            transitions.append("volume-provisioned")
            created = True
        volume.claim_key = claim.key
        volume.phase = "Bound"
        claim.selected_zone = zone
        claim.bound_volume = volume.name
        claim.phase = "Bound"
        transitions.extend(["volume-bound", "claim-bound"])
        return BindingResult(claim, volume, created, tuple(transitions))

    def release(self, claim: Claim) -> Volume:
        if claim.phase != "Bound" or not claim.bound_volume:
            raise BindingError("claim is not bound")
        volume = self.volumes[claim.bound_volume]
        claim.phase = "Released"
        volume.phase = "Released"
        return volume
