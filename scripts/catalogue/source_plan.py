"""Pure catalogue projection from captured original bytes and explicit environment."""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from hashlib import sha256
from pathlib import PurePosixPath
from typing import Any

import yaml

from scripts.catalogue.links import rewrite_markdown_links
from scripts.docs_nav import MARKDOWN_LINK_RE, directory_sort_key, normalize_link_target, _prefix_nav_item


class PlanError(ValueError):
    """Original inputs or derived catalogue ownership are inconsistent."""


def safe_path(value: str) -> str:
    if (not isinstance(value, str) or not value or "\\" in value
            or any(ord(char) < 32 or ord(char) == 127 for char in value)
            or PurePosixPath(value).is_absolute()
            or any(part in {"", ".", ".."} for part in value.split("/"))):
        raise PlanError(f"unsafe catalogue path: {value!r}")
    return value


def source_bytes(entries: Mapping[str, bytes] | Iterable[tuple[str, bytes]]) -> dict[str, bytes]:
    originals: dict[str, bytes] = {}
    for name, content in entries.items() if isinstance(entries, Mapping) else entries:
        name = safe_path(name)
        if name in originals:
            raise PlanError(f"duplicate original source: {name}")
        if not isinstance(content, bytes):
            raise PlanError(f"original source is not captured bytes: {name}")
        originals[name] = content
    return originals


@dataclass(frozen=True)
class Document:
    source: str
    destination: str
    content: bytes


@dataclass(frozen=True)
class Configuration:
    owner: str
    destination: str
    inputs: tuple[str, ...]
    navigation_configs: tuple[str, ...]
    environment: tuple[tuple[str, str], ...]
    content: bytes


@dataclass(frozen=True)
class CataloguePlan:
    documents: tuple[Document, ...]
    configuration: Configuration
    source_hashes: tuple[tuple[str, str], ...]
    families: tuple[str, ...]

    def output_bytes(self) -> dict[str, bytes]:
        return {**{item.destination: item.content for item in self.documents},
                self.configuration.destination: self.configuration.content}


def _yaml(content: bytes, name: str, environment: Mapping[str, str], resolved: dict[str, str]) -> dict[str, Any]:
    class Loader(yaml.SafeLoader):
        pass

    def mapping(loader, node, deep=False):
        keys = set()
        for key, _ in node.value:
            if key.tag == "tag:yaml.org,2002:merge":
                continue
            key = loader.construct_object(key, deep=deep)
            if key in keys:
                raise PlanError(f"duplicate configuration key in {name}: {key}")
            keys.add(key)
        return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)

    def env(loader, node):
        if isinstance(node, yaml.ScalarNode):
            key = loader.construct_scalar(node)
            if key in environment:
                resolved[key] = environment[key]
            return environment.get(key, "")
        values = loader.construct_sequence(node)
        if not values:
            return ""
        key = str(values[0])
        if key in environment:
            resolved[key] = environment[key]
        return environment.get(key, str(values[1]) if len(values) > 1 else "")

    Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    Loader.add_constructor("!ENV", env)
    data = yaml.load(content.decode("utf-8"), Loader=Loader)
    if not isinstance(data, dict):
        raise PlanError(f"configuration is not a mapping: {name}")
    return data


def build_plan(entries: Mapping[str, bytes] | Iterable[tuple[str, bytes]], *,
               environment: Mapping[str, str] | None = None) -> CataloguePlan:
    """Derive all outputs without reading files, Git, the process environment or clock."""
    originals = source_bytes(entries)
    environment = dict(environment or {})
    if any(not isinstance(key, str) or not isinstance(value, str)
           for key, value in environment.items()):
        raise PlanError("catalogue environment must contain string names and values")
    resolved_environment: dict[str, str] = {}

    def required(name: str) -> bytes:
        if name not in originals:
            raise PlanError(f"missing original source: {name}")
        return originals[name]

    config = _yaml(required("mkdocs.yml"), "mkdocs.yml", environment, resolved_environment)
    required("mkdocs.shared.yml")
    if config.get("INHERIT") != "mkdocs.shared.yml":
        raise PlanError("catalogue owner must inherit the captured mkdocs.shared.yml")
    families = sorted({name.split("/")[1] for name in originals
                       if name.startswith("programs/") and len(name.split("/")) >= 3})
    destinations: dict[str, Document] = {}

    def document(source: str, destination: str, capstone=False):
        safe_path(destination)
        if destination in destinations:
            raise PlanError(f"duplicate public destination: {destination}")
        content = rewrite_markdown_links(required(source).decode("utf-8"),
                                        capstone_docs_public_parent=capstone).encode("utf-8")
        destinations[destination] = Document(source, destination, content)

    document("programs/README.md", "docs/index.md")
    for family in families:
        document(f"programs/{family}/README.md", f"docs/{family}/index.md")
    programs: dict[str, set[str]] = {family: set() for family in families}
    for name in sorted(originals):
        parts = name.split("/")
        if len(parts) < 5 or parts[0] != "programs" or not name.endswith(".md"):
            continue
        family, program = parts[1:3]
        if parts[3] == "course-book":
            document(name, "/".join(["docs", family, program, *parts[4:]]))
            programs[family].add(program)
        elif len(parts) >= 6 and parts[3:5] == ["capstone", "docs"]:
            document(name, "/".join(["docs", family, program, "capstone-docs", *parts[5:]]), True)
            programs[family].add(program)

    nav = config.get("nav")
    if not isinstance(nav, list) or not nav:
        raise PlanError("missing root catalogue navigation")
    if nav[0] != {"Home": "index.md"}:
        raise PlanError("root catalogue Home must own index.md")
    generated = [nav[0]]
    config_inputs = {"mkdocs.yml", "mkdocs.shared.yml"}
    used_families = set()
    for item in nav[1:]:
        if not isinstance(item, dict) or len(item) != 1:
            raise PlanError("family navigation must have one authored label")
        label, home = next(iter(item.items()))
        safe_path(home)
        parts = home.split("/")
        if len(parts) != 2 or parts[1] != "index.md" or parts[0] not in programs:
            raise PlanError(f"unknown family navigation: {home}")
        family = parts[0]
        if family in used_families:
            raise PlanError(f"duplicate family navigation: {family}")
        used_families.add(family)
        order = {}
        index = destinations[f"docs/{family}/index.md"].content.decode("utf-8")
        for match in MARKDOWN_LINK_RE.finditer(index):
            target = normalize_link_target(match[1])
            first = target.split("/")[0]
            if first in programs[family]:
                order.setdefault(first, len(order))

        def sort_program(name):
            group, number, slug = directory_sort_key(PurePosixPath(name))
            return order.get(name, 10_000), group, number, slug

        family_nav = [{"Home": home}]
        for program in sorted(programs[family], key=sort_program):
            owner = f"programs/{family}/{program}/mkdocs.yml"
            course = _yaml(required(owner), owner, environment, resolved_environment)
            config_inputs.add(owner)
            course_nav = course.get("nav")
            if not isinstance(course_nav, list):
                raise PlanError(f"missing explicit course nav in {owner}")
            child = [_prefix_nav_item(value, f"{family}/{program}") for value in course_nav]
            family_nav.append({str(course.get("site_name", program.replace("-", " ").title())): child})
        generated.append({label: family_nav})
    if used_families != set(families):
        raise PlanError("root navigation omits an original catalogue family")

    def verify_nav(value):
        if isinstance(value, str):
            safe_path(value)
            if f"docs/{value}" not in destinations:
                raise PlanError(f"navigation has no planned document: {value}")
        elif isinstance(value, list):
            for item in value:
                verify_nav(item)
        elif isinstance(value, dict):
            for item in value.values():
                verify_nav(item)
        else:
            raise PlanError("unsupported navigation entry")
    verify_nav(generated)
    config["nav"] = generated
    if isinstance(config.get("watch"), list):
        config["watch"] = [entry if not isinstance(entry, str) or entry.startswith(("/", "../"))
                           else "../" + entry.removeprefix("./") for entry in config["watch"]]
    config.update(INHERIT="../mkdocs.shared.yml", docs_dir="../docs", site_dir="site/bijux-masterclass")
    theme = config.setdefault("theme", {})
    if not isinstance(theme, dict):
        raise PlanError("unsupported root theme configuration")
    theme["custom_dir"] = "../docs/overrides"
    config["hooks"] = ["../docs/hooks/publish_site_assets.py"]
    configuration = Configuration("mkdocs.yml", "artifacts/mkdocs.root.yml",
                                  tuple(sorted(originals)),
                                  tuple(sorted(config_inputs - {"mkdocs.yml", "mkdocs.shared.yml"})),
                                  tuple(sorted(resolved_environment.items())),
                                  yaml.safe_dump(config, allow_unicode=True, sort_keys=False).encode("utf-8"))
    return CataloguePlan(tuple(destinations[key] for key in sorted(destinations)), configuration,
                         tuple((key, sha256(originals[key]).hexdigest()) for key in sorted(originals)),
                         tuple(families))
