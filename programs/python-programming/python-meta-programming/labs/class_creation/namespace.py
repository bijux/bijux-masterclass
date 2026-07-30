from __future__ import annotations


class DeclarationNamespace(dict[str, object]):
    """Record public declaration order and reject duplicate public names."""

    def __init__(self) -> None:
        super().__init__()
        self.public_names: list[str] = []

    def __setitem__(self, key: str, value: object) -> None:
        if not key.startswith("__"):
            if key in self:
                raise TypeError(f"duplicate public declaration: {key}")
            self.public_names.append(key)
        super().__setitem__(key, value)


class DeclarationMeta(type):
    """Preserve facts that exist only while the class body executes."""

    @classmethod
    def __prepare__(
        mcs,
        name: str,
        bases: tuple[type[object], ...],
    ) -> DeclarationNamespace:
        return DeclarationNamespace()

    def __new__(
        mcs,
        name: str,
        bases: tuple[type[object], ...],
        namespace: DeclarationNamespace,
    ) -> DeclarationMeta:
        namespace["__declaration_order__"] = tuple(namespace.public_names)
        return super().__new__(mcs, name, bases, namespace)


def namespace_evidence() -> dict[str, object]:
    """Contrast declaration-time observation with final namespace inspection."""

    class DeliveryPolicy(metaclass=DeclarationMeta):
        channel = "console"
        attempts = 3

        def deliver(self: object) -> str:
            return "delivered"

    failure_message = ""
    try:

        class DuplicatePolicy(metaclass=DeclarationMeta):
            channel = "console"
            channel = "webhook"

    except TypeError as error:
        failure_message = str(error)

    class PlainPolicy:
        channel = "console"
        channel = "webhook"

    return {
        "prepared_namespace": {
            "type": DeclarationNamespace.__name__,
            "public_declaration_order": list(
                DeliveryPolicy.__declaration_order__
            ),
            "final_public_names": [
                name for name in vars(DeliveryPolicy) if not name.startswith("__")
            ],
        },
        "duplicate_rule": {
            "failure_type": "TypeError",
            "message": failure_message,
            "class_bound": "DuplicatePolicy" in locals(),
        },
        "plain_mapping_limit": {
            "visible_value": PlainPolicy.channel,
            "duplicate_event_recoverable_after_creation": False,
        },
        "claim_limits": [
            "__prepare__ selects the mapping used during class-body execution",
            "a custom mapping should preserve a fact that later inspection loses",
            "ordinary declaration order alone does not require a custom mapping",
        ],
    }
