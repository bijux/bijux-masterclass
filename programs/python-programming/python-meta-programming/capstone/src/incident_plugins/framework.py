from __future__ import annotations

from collections import OrderedDict, defaultdict
import inspect
from typing import Any

from .actions import ActionSpec
from .fields import Field


_REGISTRY: dict[str, dict[str, type["PluginBase"]]] = defaultdict(dict)


class DefinitionNamespace(OrderedDict[str, object]):
    """Reject accidental duplicate tracked members during class-body execution."""

    def __setitem__(self, key: str, value: object) -> None:
        if key in self and (_is_tracked(self[key]) or _is_tracked(value)):
            raise TypeError(f"duplicate tracked definition for {key!r}")
        super().__setitem__(key, value)


def _build_signature(fields: OrderedDict[str, Field]) -> inspect.Signature:
    parameters = []
    for name, field in fields.items():
        default = inspect._empty if field.required() else field.default
        parameters.append(
            inspect.Parameter(name, inspect.Parameter.KEYWORD_ONLY, default=default)
        )
    return inspect.Signature(parameters)


def _build_init(fields: OrderedDict[str, Field]):
    signature = _build_signature(fields)

    def __init__(self, *args: object, **kwargs: object) -> None:
        bound = signature.bind(*args, **kwargs)
        values = dict(bound.arguments)
        self._action_history: list[dict[str, object]] = []
        for field in fields.values():
            field.initialize(self, values)

    __init__.__signature__ = signature
    return __init__


def _inherit_group(bases: tuple[type[object], ...]) -> str | None:
    for base in bases:
        group = getattr(base, "group", None)
        if group is not None:
            return group
    return None


def _register_plugin(plugin_cls: type["PluginBase"]) -> None:
    group_bucket = _REGISTRY[plugin_cls.group]
    if plugin_cls.plugin_name in group_bucket:
        raise ValueError(
            f"duplicate plugin name {plugin_cls.plugin_name!r} in group {plugin_cls.group!r}"
        )
    group_bucket[plugin_cls.plugin_name] = plugin_cls


def _to_slug(name: str) -> str:
    letters = []
    for char in name:
        if char.isupper() and letters:
            letters.append("-")
        letters.append(char.lower())
    return "".join(letters)


def _is_tracked(value: object) -> bool:
    return isinstance(value, Field) or hasattr(value, "__plugin_action__")


class PluginMeta(type):
    @classmethod
    def __prepare__(mcs, name: str, bases: tuple[type[object], ...], **kwargs: object) -> DefinitionNamespace:
        return DefinitionNamespace()

    def __new__(
        mcs,
        name: str,
        bases: tuple[type[object], ...],
        namespace: dict[str, object],
        **kwargs: object,
    ) -> "PluginMeta":
        cls = super().__new__(mcs, name, bases, dict(namespace))

        fields: OrderedDict[str, Field] = OrderedDict()
        actions: OrderedDict[str, ActionSpec] = OrderedDict()
        for base in bases:
            fields.update(getattr(base, "__plugin_fields__", {}))
            actions.update(getattr(base, "__plugin_actions__", {}))

        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
            spec = getattr(attr_value, "__plugin_action__", None)
            if spec is not None:
                actions[attr_name] = spec

        cls.__plugin_fields__ = fields
        cls.__plugin_actions__ = actions
        cls.__signature__ = _build_signature(fields)

        if "__init__" not in namespace:
            cls.__init__ = _build_init(fields)

        is_abstract = bool(namespace.get("__abstract__", False))
        cls.__abstract__ = is_abstract
        if is_abstract:
            return cls

        group = getattr(cls, "group", None) or _inherit_group(bases) or "default"
        plugin_name = getattr(cls, "plugin_name", None) or _to_slug(name)
        cls.group = group
        cls.plugin_name = plugin_name
        _register_plugin(cls)
        return cls

    @classmethod
    def registry(cls, group: str | None = None) -> dict[str, tuple[str, ...]] | tuple[str, ...]:
        if group is not None:
            return tuple(sorted(_REGISTRY.get(group, {}).keys()))
        return {name: tuple(sorted(items.keys())) for name, items in sorted(_REGISTRY.items())}

    @classmethod
    def clear_registry(cls, group: str | None = None) -> None:
        if group is None:
            _REGISTRY.clear()
            return
        _REGISTRY.pop(group, None)


class PluginBase(metaclass=PluginMeta):
    __abstract__ = True
    group = "default"

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise NotImplementedError("PluginMeta replaces __init__ on concrete subclasses")

    @classmethod
    def manifest(cls) -> dict[str, object]:
        return {
            "group": cls.group,
            "plugin_name": cls.plugin_name,
            "fields": [field.spec().manifest() for field in cls.__plugin_fields__.values()],
            "actions": [spec.manifest() for spec in cls.__plugin_actions__.values()],
            "doc": inspect.getdoc(cls) or "",
        }

    def configuration(self) -> dict[str, object]:
        return {name: getattr(self, name) for name in self.__plugin_fields__}

    def action_history(self) -> list[dict[str, object]]:
        return list(self._action_history)


def build_manifest(group: str | None = None) -> dict[str, list[dict[str, object]]]:
    groups = [group] if group is not None else sorted(_REGISTRY)
    return {
        group_name: [
            _REGISTRY[group_name][plugin_name].manifest()
            for plugin_name in sorted(_REGISTRY.get(group_name, {}))
        ]
        for group_name in groups
    }


def create_plugin(group: str, plugin_name: str, **config: object) -> PluginBase:
    plugin_cls = _REGISTRY[group][plugin_name]
    return plugin_cls(**config)


def invoke(
    group: str,
    plugin_name: str,
    action_name: str,
    *,
    config: dict[str, object] | None = None,
    **kwargs: object,
) -> object:
    plugin = create_plugin(group, plugin_name, **(config or {}))
    method = getattr(plugin, action_name)
    return method(**kwargs)
