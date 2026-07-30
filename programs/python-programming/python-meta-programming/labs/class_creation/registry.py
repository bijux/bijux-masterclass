from __future__ import annotations

from collections import defaultdict


class PluginRegistry:
    """Deterministic, resettable bookkeeping kept outside the metaclass."""

    def __init__(self) -> None:
        self._groups: dict[str, dict[str, type[object]]] = defaultdict(dict)

    def register(
        self,
        group: str,
        plugin_name: str,
        plugin_class: type[object],
    ) -> None:
        group_entries = self._groups[group]
        if plugin_name in group_entries:
            raise ValueError(
                f"duplicate plugin {plugin_name!r} in group {group!r}"
            )
        group_entries[plugin_name] = plugin_class

    def names(self, group: str) -> tuple[str, ...]:
        return tuple(sorted(self._groups.get(group, {})))

    def resolve(self, group: str, plugin_name: str) -> type[object]:
        return self._groups[group][plugin_name]

    def clear(self, group: str | None = None) -> None:
        if group is None:
            self._groups.clear()
            return
        self._groups.pop(group, None)


def _slug(name: str) -> str:
    pieces: list[str] = []
    for character in name:
        if character.isupper() and pieces:
            pieces.append("-")
        pieces.append(character.lower())
    return "".join(pieces)


def make_plugin_family(
    registry: PluginRegistry,
) -> tuple[type[type[object]], type[object]]:
    """Create one isolated class family with automatic concrete registration."""

    class PluginMeta(type):
        def __new__(
            mcs,
            name: str,
            bases: tuple[type[object], ...],
            namespace: dict[str, object],
        ) -> PluginMeta:
            cls = super().__new__(mcs, name, bases, namespace)
            cls.__abstract__ = bool(namespace.get("__abstract__", False))
            inherited_group = next(
                (
                    str(base.group)
                    for base in bases
                    if getattr(base, "group", None) is not None
                ),
                "default",
            )
            cls.group = str(namespace.get("group", inherited_group))
            cls.plugin_name = str(namespace.get("plugin_name", _slug(name)))
            cls.__creation_trace__ = (f"new:{name}:shape",)
            return cls

        def __init__(
            cls,
            name: str,
            bases: tuple[type[object], ...],
            namespace: dict[str, object],
        ) -> None:
            super().__init__(name, bases, namespace)
            cls.__creation_trace__ = (
                *cls.__creation_trace__,
                f"init:{name}:bookkeeping",
            )
            if cls.__abstract__:
                return
            registry.register(cls.group, cls.plugin_name, cls)
            cls.__creation_trace__ = (
                *cls.__creation_trace__,
                f"register:{cls.group}:{cls.plugin_name}",
            )

    class PluginBase(metaclass=PluginMeta):
        __abstract__ = True
        group = "default"

    return PluginMeta, PluginBase


def registry_evidence() -> dict[str, object]:
    """Build an isolated registry and expose policy, bookkeeping, and failure."""

    registry = PluginRegistry()
    _, PluginBase = make_plugin_family(registry)

    class DeliveryPlugin(PluginBase):
        __abstract__ = True
        group = "delivery"

    class WebhookPlugin(DeliveryPlugin):
        plugin_name = "webhook"

    class ConsolePlugin(DeliveryPlugin):
        plugin_name = "console"

    duplicate_message = ""
    try:

        class DuplicateConsole(DeliveryPlugin):
            plugin_name = "console"

    except ValueError as error:
        duplicate_message = str(error)

    names_before_clear = registry.names("delivery")
    resolved = registry.resolve("delivery", "console")
    registry.clear("delivery")

    return {
        "abstract_policy": {
            "base_registered": bool(registry.names("default")),
            "family_registered": "delivery-plugin" in names_before_clear,
        },
        "concrete_plugins": {
            "names_before_clear": list(names_before_clear),
            "resolved_console_class": resolved.__name__,
            "console_creation_trace": list(ConsolePlugin.__creation_trace__),
            "webhook_creation_trace": list(WebhookPlugin.__creation_trace__),
        },
        "duplicate": {
            "failure_type": "ValueError",
            "message": duplicate_message,
            "original_preserved": resolved is ConsolePlugin,
        },
        "reset": {
            "names_after_clear": list(registry.names("delivery")),
            "owner": PluginRegistry.__name__,
        },
        "claim_limits": [
            "the metaclass guarantees registration for this in-process class family",
            "the registry owns ordering, lookup, duplicates, and reset",
            "neither component discovers packages or coordinates processes",
        ],
    }
