from __future__ import annotations

from dataclasses import asdict, dataclass
from ipaddress import ip_network


@dataclass(slots=True)
class Attachment:
    network: str
    attachment_id: str
    container_id: str
    pod_uid: str
    interface: str
    address: str
    generation: int
    active: bool = True


class CNIState:
    """Small semantic model of CNI attachment and IPAM ownership.

    It deliberately does not mutate Linux namespaces. The model exists to make
    replay, generation conflicts, partial failure, and garbage collection
    deterministic for the course laboratories.
    """

    def __init__(self, pool: str):
        self.pool = ip_network(pool, strict=False)
        self.attachments: dict[str, Attachment] = {}
        self.actions: list[dict[str, object]] = []

    def _available(self) -> str:
        allocated = {
            attachment.address
            for attachment in self.attachments.values()
            if attachment.active
        }
        for address in self.pool.hosts():
            candidate = str(address)
            if candidate not in allocated:
                return candidate
        raise RuntimeError("address pool exhausted")

    def add(
        self,
        *,
        network: str,
        attachment_id: str,
        container_id: str,
        pod_uid: str,
        interface: str,
        generation: int,
        fail_after_allocate: bool = False,
    ) -> Attachment:
        existing = self.attachments.get(attachment_id)
        if existing and existing.active:
            same_identity = (
                existing.container_id,
                existing.pod_uid,
                existing.generation,
            ) == (container_id, pod_uid, generation)
            if same_identity:
                self.actions.append(
                    {
                        "command": "ADD",
                        "attachment": attachment_id,
                        "result": "replay",
                    }
                )
                return existing
            raise RuntimeError("attachment identity conflict")

        address = self._available()
        attachment = Attachment(
            network=network,
            attachment_id=attachment_id,
            container_id=container_id,
            pod_uid=pod_uid,
            interface=interface,
            address=address,
            generation=generation,
            active=not fail_after_allocate,
        )
        self.attachments[attachment_id] = attachment
        self.actions.append(
            {
                "command": "ADD",
                "attachment": attachment_id,
                "address": address,
                "result": "partial" if fail_after_allocate else "success",
            }
        )
        if fail_after_allocate:
            raise RuntimeError("injected interface failure after IP allocation")
        return attachment

    def check(self, attachment_id: str) -> bool:
        attachment = self.attachments.get(attachment_id)
        present = bool(attachment and attachment.active)
        self.actions.append(
            {
                "command": "CHECK",
                "attachment": attachment_id,
                "result": "success" if present else "missing",
            }
        )
        return present

    def delete(self, attachment_id: str) -> bool:
        attachment = self.attachments.get(attachment_id)
        if not attachment or not attachment.active:
            self.actions.append(
                {
                    "command": "DEL",
                    "attachment": attachment_id,
                    "result": "absent",
                }
            )
            return True

        attachment.active = False
        self.actions.append(
            {
                "command": "DEL",
                "attachment": attachment_id,
                "result": "removed",
            }
        )
        return True

    def gc(self, known_good: set[tuple[str, int]]) -> list[str]:
        removed: list[str] = []
        for attachment_id, attachment in self.attachments.items():
            identity = (attachment_id, attachment.generation)
            if attachment.active and identity not in known_good:
                attachment.active = False
                removed.append(attachment_id)
                self.actions.append(
                    {
                        "command": "GC",
                        "attachment": attachment_id,
                        "result": "removed",
                    }
                )
        return sorted(removed)

    def unsafe_gc_by_pod_name(self, active_pod_names: set[str]) -> list[str]:
        """Deliberate mutant used by the planted-defect proof."""

        removed: list[str] = []
        for attachment_id, attachment in self.attachments.items():
            pod_name = attachment.pod_uid.split(":", 1)[0]
            if attachment.active and pod_name not in active_pod_names:
                attachment.active = False
                removed.append(attachment_id)
        return sorted(removed)

    @staticmethod
    def status(dependencies: dict[str, bool]) -> bool:
        return all(dependencies.values())

    def snapshot(self) -> list[dict[str, object]]:
        return [
            asdict(attachment)
            for attachment in sorted(
                self.attachments.values(),
                key=lambda item: item.attachment_id,
            )
        ]
