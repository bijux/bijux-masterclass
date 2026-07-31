from __future__ import annotations


def lifecycle_evidence() -> dict[str, object]:
    """Trace class body, metaclass hooks, binding, and later construction."""

    events: list[str] = []
    registry: list[str] = []

    class LifecycleMeta(type):
        @classmethod
        def __prepare__(
            mcs,
            name: str,
            bases: tuple[type[object], ...],
        ) -> dict[str, object]:
            events.append(f"prepare:{name}")
            return {}

        def __new__(
            mcs,
            name: str,
            bases: tuple[type[object], ...],
            namespace: dict[str, object],
        ) -> LifecycleMeta:
            events.append(f"new:{name}")
            namespace["creation_owner"] = mcs.__name__
            return super().__new__(mcs, name, bases, namespace)

        def __init__(
            cls,
            name: str,
            bases: tuple[type[object], ...],
            namespace: dict[str, object],
        ) -> None:
            super().__init__(name, bases, namespace)
            events.append(f"init:{name}")
            registry.append(cls.__name__)

    class DeliveryNotice(metaclass=LifecycleMeta):
        events.append("body:DeliveryNotice")
        channel = "console"

    events_after_class_statement = list(events)
    bound_class_name = DeliveryNotice.__name__
    notice = DeliveryNotice()
    events_after_instance = list(events)

    failure_events: list[str] = []

    class RequiredChannelMeta(type):
        def __new__(
            mcs,
            name: str,
            bases: tuple[type[object], ...],
            namespace: dict[str, object],
        ) -> RequiredChannelMeta:
            failure_events.append(f"new:{name}")
            if "channel" not in namespace:
                raise TypeError(f"{name} must declare channel")
            return super().__new__(mcs, name, bases, namespace)

        def __init__(
            cls,
            name: str,
            bases: tuple[type[object], ...],
            namespace: dict[str, object],
        ) -> None:
            failure_events.append(f"init:{name}")
            super().__init__(name, bases, namespace)

    failure_message = ""
    try:

        class MissingChannel(metaclass=RequiredChannelMeta):
            pass

    except TypeError as error:
        failure_message = str(error)

    return {
        "successful_class": {
            "events": events_after_class_statement,
            "bound_name": bound_class_name,
            "creation_owner": DeliveryNotice.creation_owner,
            "registered_names": registry,
        },
        "instance": {
            "type": type(notice).__name__,
            "events_after_construction": events_after_instance,
            "metaclass_hooks_reran": (
                events_after_instance != events_after_class_statement
            ),
        },
        "rejected_class": {
            "events": failure_events,
            "failure_type": "TypeError",
            "message": failure_message,
            "init_ran": any(event.startswith("init:") for event in failure_events),
        },
        "ownership": {
            "prepare": "choose the class-body namespace",
            "body": "execute declarations into that namespace",
            "new": "validate or shape the class before returning it",
            "init": "initialize or record the returned class",
            "call": "construct an instance later",
        },
    }
