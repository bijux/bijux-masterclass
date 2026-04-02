from __future__ import annotations

import argparse
import json
import inspect
from typing import Any

from .framework import PluginMeta, _REGISTRY, build_manifest, create_plugin, invoke


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    payload = args.handler(args)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="incident-plugins",
        description="Inspect and exercise the incident plugin runtime.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    manifest = subparsers.add_parser("manifest", help="Render the runtime manifest as JSON.")
    manifest.add_argument("--group", help="Restrict output to one plugin group.")
    manifest.set_defaults(handler=_handle_manifest)

    plugin = subparsers.add_parser(
        "plugin",
        help="Render the manifest entry for one concrete plugin.",
    )
    plugin.add_argument("group", help="Plugin group name.")
    plugin.add_argument("plugin_name", help="Registered plugin name.")
    plugin.set_defaults(handler=_handle_plugin)

    field = subparsers.add_parser(
        "field",
        help="Render one field contract for one concrete plugin.",
    )
    field.add_argument("group", help="Plugin group name.")
    field.add_argument("plugin_name", help="Registered plugin name.")
    field.add_argument("field_name", help="Declared field name.")
    field.set_defaults(handler=_handle_field)

    registry = subparsers.add_parser("registry", help="Render the plugin registry as JSON.")
    registry.add_argument("--group", help="Restrict output to one plugin group.")
    registry.set_defaults(handler=_handle_registry)

    signatures = subparsers.add_parser(
        "signatures",
        help="Render generated constructor and action signatures as JSON.",
    )
    signatures.add_argument("--group", help="Restrict output to one plugin group.")
    signatures.set_defaults(handler=_handle_signatures)

    invoke_parser = subparsers.add_parser("invoke", help="Invoke one plugin action and print the result.")
    _add_runtime_arguments(invoke_parser)
    invoke_parser.set_defaults(handler=_handle_invoke)

    trace = subparsers.add_parser(
        "trace",
        help="Invoke one plugin action and print result, configuration, and action history.",
    )
    _add_runtime_arguments(trace)
    trace.set_defaults(handler=_handle_trace)

    return parser


def _add_runtime_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("group", help="Plugin group name.")
    parser.add_argument("plugin_name", help="Registered plugin name.")
    parser.add_argument("action_name", help="Action method to invoke.")
    parser.add_argument(
        "--config",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Plugin configuration entry. May be repeated.",
    )
    parser.add_argument(
        "--arg",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Action argument entry. May be repeated.",
    )


def _handle_manifest(args: argparse.Namespace) -> dict[str, list[dict[str, object]]]:
    return build_manifest(args.group)


def _handle_plugin(args: argparse.Namespace) -> dict[str, object]:
    plugin_cls = _REGISTRY[args.group][args.plugin_name]
    return plugin_cls.manifest()


def _handle_field(args: argparse.Namespace) -> dict[str, object]:
    plugin_cls = _REGISTRY[args.group][args.plugin_name]
    field = plugin_cls.__plugin_fields__[args.field_name]
    return {
        "group": args.group,
        "plugin_name": args.plugin_name,
        "field": field.spec().manifest(),
    }


def _handle_registry(args: argparse.Namespace) -> dict[str, Any]:
    registry = PluginMeta.registry(args.group)
    if args.group is not None:
        return {"group": args.group, "plugins": list(registry)}
    return {group: list(plugins) for group, plugins in registry.items()}


def _handle_signatures(args: argparse.Namespace) -> dict[str, list[dict[str, object]]]:
    groups = [args.group] if args.group is not None else sorted(_REGISTRY)
    return {
        group_name: [
            {
                "plugin_name": plugin_name,
                "constructor": str(inspect.signature(plugin_cls)),
                "actions": {
                    action_name: str(inspect.signature(getattr(plugin_cls, action_name)))
                    for action_name in plugin_cls.__plugin_actions__
                },
            }
            for plugin_name, plugin_cls in sorted(_REGISTRY.get(group_name, {}).items())
        ]
        for group_name in groups
    }


def _handle_invoke(args: argparse.Namespace) -> dict[str, object]:
    result = invoke(
        args.group,
        args.plugin_name,
        args.action_name,
        config=_parse_key_values(args.config),
        **_parse_key_values(args.arg),
    )
    return {
        "group": args.group,
        "plugin_name": args.plugin_name,
        "action_name": args.action_name,
        "result": result,
    }


def _handle_trace(args: argparse.Namespace) -> dict[str, object]:
    config = _parse_key_values(args.config)
    action_args = _parse_key_values(args.arg)
    plugin = create_plugin(args.group, args.plugin_name, **config)
    method = getattr(plugin, args.action_name)
    result = method(**action_args)
    return {
        "group": args.group,
        "plugin_name": args.plugin_name,
        "action_name": args.action_name,
        "configuration": plugin.configuration(),
        "history": plugin.action_history(),
        "result": result,
    }


def _parse_key_values(items: list[str]) -> dict[str, object]:
    values: dict[str, object] = {}
    for item in items:
        key, separator, raw_value = item.partition("=")
        if not separator or not key:
            raise SystemExit(f"expected KEY=VALUE, got {item!r}")
        values[key] = _coerce_scalar(raw_value)
    return values


def _coerce_scalar(raw_value: str) -> object:
    text = raw_value.strip()
    lowered = text.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        return int(text)
    except ValueError:
        return text


if __name__ == "__main__":
    raise SystemExit(main())
