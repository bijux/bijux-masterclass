from __future__ import annotations

from collections import OrderedDict, defaultdict
from dataclasses import asdict, dataclass
import inspect
from typing import Any

from .actions import (
    ActionSpec,
    check_action_values,
    describe_action_wrapper,
    resolve_action_hints,
)
from .fields import Field


_REGISTRY: dict[str, dict[str, type["PluginBase"]]] = defaultdict(dict)


@dataclass(frozen=True, slots=True)
class ClassCreationSpec:
    """Evidence captured while ``PluginMeta`` still owns class creation."""

    namespace_type: str
    metaclass: str
    declared_fields: tuple[str, ...]
    declared_actions: tuple[str, ...]
    inherited_fields: tuple[str, ...]
    inherited_actions: tuple[str, ...]
    generated_init: bool
    abstract: bool

    def manifest(self) -> dict[str, object]:
        return asdict(self)


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
        inherited_fields = tuple(fields)
        inherited_actions = tuple(actions)

        declared_fields = []
        declared_actions = []
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
                declared_fields.append(attr_name)
            spec = getattr(attr_value, "__plugin_action__", None)
            if spec is not None:
                actions[attr_name] = spec
                declared_actions.append(attr_name)

        cls.__plugin_fields__ = fields
        cls.__plugin_actions__ = actions
        cls.__signature__ = _build_signature(fields)

        generated_init = "__init__" not in namespace
        if generated_init:
            cls.__init__ = _build_init(fields)

        is_abstract = bool(namespace.get("__abstract__", False))
        cls.__abstract__ = is_abstract
        cls.__plugin_class_creation__ = ClassCreationSpec(
            namespace_type=type(namespace).__name__,
            metaclass=type(cls).__name__,
            declared_fields=tuple(declared_fields),
            declared_actions=tuple(declared_actions),
            inherited_fields=inherited_fields,
            inherited_actions=inherited_actions,
            generated_init=generated_init,
            abstract=is_abstract,
        )
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


def bind_action_arguments(
    group: str,
    plugin_name: str,
    action_name: str,
    *args: object,
    **kwargs: object,
) -> dict[str, object]:
    """Validate an action call without constructing or invoking the plugin."""

    plugin_cls = _REGISTRY[group][plugin_name]
    action_spec = plugin_cls.__plugin_actions__[action_name]
    bound = action_spec.signature.bind(None, *args, **kwargs)
    bound.apply_defaults()
    return {
        name: value
        for name, value in bound.arguments.items()
        if name != "self"
    }


def inspect_action_wrapper(
    group: str,
    plugin_name: str,
    action_name: str,
) -> dict[str, object]:
    """Inspect a registered action wrapper without construction or invocation."""

    plugin_cls = _REGISTRY[group][plugin_name]
    function = inspect.getattr_static(plugin_cls, action_name)
    return {
        "group": group,
        "plugin_name": plugin_name,
        "action_name": action_name,
        "constructed": False,
        "executed": False,
        "wrapper": describe_action_wrapper(function),
    }


def check_action_arguments(
    group: str,
    plugin_name: str,
    action_name: str,
    *args: object,
    **kwargs: object,
) -> dict[str, object]:
    """Check the supported action-hint subset without constructing or invoking."""

    bound_arguments = bind_action_arguments(
        group,
        plugin_name,
        action_name,
        *args,
        **kwargs,
    )
    plugin_cls = _REGISTRY[group][plugin_name]
    action_spec = plugin_cls.__plugin_actions__[action_name]
    function = inspect.getattr_static(plugin_cls, action_name)
    resolved_hints, resolution_error = resolve_action_hints(inspect.unwrap(function))
    return {
        "group": group,
        "plugin_name": plugin_name,
        "action_name": action_name,
        "bound_arguments": bound_arguments,
        **check_action_values(
            action_spec,
            bound_arguments,
            resolved_hints,
            resolution_error,
        ),
        "constructed": False,
        "executed": False,
    }


def inspect_plugin_class_creation(
    group: str,
    plugin_name: str,
) -> dict[str, object]:
    """Expose one stored class-creation record without constructing the plugin."""

    plugin_cls = _REGISTRY[group][plugin_name]
    creation = plugin_cls.__plugin_class_creation__
    return {
        "group": group,
        "plugin_name": plugin_name,
        "class_name": plugin_cls.__name__,
        "class_creation": creation.manifest(),
        "visible_signature": str(inspect.signature(plugin_cls)),
        "collected_fields": list(plugin_cls.__plugin_fields__),
        "collected_actions": list(plugin_cls.__plugin_actions__),
        "registered": plugin_name in _REGISTRY.get(group, {}),
        "constructed": False,
        "executed": False,
    }


def inspect_field_ownership(
    group: str,
    plugin_name: str,
    field_name: str,
) -> dict[str, object]:
    """Inspect one field descriptor without constructing the plugin."""

    plugin_cls = _REGISTRY[group][plugin_name]
    descriptor = inspect.getattr_static(plugin_cls, field_name)
    if not isinstance(descriptor, Field):
        raise TypeError(f"{field_name!r} is not a plugin field")
    declaring_class = next(
        owner.__name__
        for owner in plugin_cls.__mro__
        if vars(owner).get(field_name) is descriptor
    )
    descriptor_type = type(descriptor)
    hooks = [
        hook
        for hook in ("__get__", "__set__", "__delete__", "__set_name__")
        if hasattr(descriptor_type, hook)
    ]
    return {
        "group": group,
        "plugin_name": plugin_name,
        "field_name": field_name,
        "declaring_class": declaring_class,
        "descriptor_type": descriptor_type.__name__,
        "descriptor_kind": (
            "data"
            if "__set__" in hooks or "__delete__" in hooks
            else "non-data"
        ),
        "hooks": hooks,
        "public_name": descriptor.name,
        "storage_name": descriptor.storage_name,
        "storage_owner": "plugin-instance.__dict__",
        "class_access_returns_descriptor": (
            getattr(plugin_cls, field_name) is descriptor
        ),
        "collected_by_metaclass": (
            plugin_cls.__plugin_fields__.get(field_name) is descriptor
        ),
        "field": descriptor.spec().manifest(),
        "constructed": False,
        "executed": False,
    }


def inspect_field_system(
    group: str,
    plugin_name: str,
) -> dict[str, object]:
    """Inspect the collected field system and its deliberate power limits."""

    plugin_cls = _REGISTRY[group][plugin_name]
    field_contracts = []
    for field_name, descriptor in plugin_cls.__plugin_fields__.items():
        descriptor_type = type(descriptor)
        coercion_owner = next(
            owner.__name__
            for owner in descriptor_type.__mro__
            if "coerce" in vars(owner)
        )
        field_contracts.append({
            "name": field_name,
            "descriptor_type": descriptor_type.__name__,
            "coercion_owner": coercion_owner,
            "storage_name": descriptor.storage_name,
            "source_of_truth": "plugin-instance.__dict__",
        })

    return {
        "group": group,
        "plugin_name": plugin_name,
        "class_name": plugin_cls.__name__,
        "fields": field_contracts,
        "accepted_powers": [
            {
                "power": "assignment coercion and validation",
                "owner": "explicit Field subclass",
            },
            {
                "power": "per-instance configuration storage",
                "owner": "plugin instance",
            },
            {
                "power": "field collection and constructor generation",
                "owner": "PluginMeta",
            },
            {
                "power": "public field schema",
                "owner": "FieldSpec manifest",
            },
        ],
        "rejected_powers": [
            {
                "power": "derived-value caching",
                "reason": "no derived configuration value requires invalidation",
            },
            {
                "power": "external storage during attribute access",
                "reason": "plugin configuration remains local and deterministic",
            },
            {
                "power": "field wrapper composition",
                "reason": "explicit field subclasses keep current policy legible",
            },
            {
                "power": "annotation-inferred field policy",
                "reason": "field classes declare runtime coercion directly",
            },
            {
                "power": "cross-field transactions",
                "reason": "configuration initialization has no persistence transaction",
            },
        ],
        "constructed": False,
        "executed": False,
    }


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
