from __future__ import annotations


def resolution_evidence() -> dict[str, object]:
    """Expose inherited metaclass selection, timing, and one real conflict."""

    creation_events: list[str] = []

    class AuditMeta(type):
        def __new__(
            mcs,
            name: str,
            bases: tuple[type[object], ...],
            namespace: dict[str, object],
        ) -> AuditMeta:
            creation_events.append(f"create:{name}")
            return super().__new__(mcs, name, bases, namespace)

    class AuditedBase(metaclass=AuditMeta):
        pass

    class DeliveryAudit(AuditedBase):
        pass

    events_before_instance = list(creation_events)
    DeliveryAudit()
    events_after_instance = list(creation_events)

    class PolicyMeta(type):
        pass

    class PolicyBase(metaclass=PolicyMeta):
        pass

    conflict_message = ""
    try:

        class Conflicted(AuditedBase, PolicyBase):
            pass

    except TypeError as error:
        conflict_message = str(error)

    class JointMeta(AuditMeta, PolicyMeta):
        pass

    class DeliberatelyCombined(
        AuditedBase,
        PolicyBase,
        metaclass=JointMeta,
    ):
        pass

    return {
        "inheritance": {
            "base_metaclass": type(AuditedBase).__name__,
            "child_metaclass": type(DeliveryAudit).__name__,
            "explicit_child_metaclass": False,
        },
        "timing": {
            "events_before_instance": events_before_instance,
            "events_after_instance": events_after_instance,
            "instance_creation_added_events": (
                len(events_after_instance) != len(events_before_instance)
            ),
        },
        "conflict": {
            "left_metaclass": type(AuditedBase).__name__,
            "right_metaclass": type(PolicyBase).__name__,
            "failure_type": "TypeError",
            "mentions_metaclass_conflict": "metaclass conflict" in conflict_message,
        },
        "combined": {
            "effective_metaclass": type(DeliberatelyCombined).__name__,
            "joint_metaclass_bases": [
                base.__name__ for base in JointMeta.__bases__
            ],
            "automatic_repair": False,
        },
        "claim_limits": [
            "a joint metaclass resolves mechanics only when its policies compose",
            "successful class creation does not prove semantic compatibility",
        ],
    }
