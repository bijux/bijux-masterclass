from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any

from .identifiers import entity_ref, parse_ref
from .models import Entity


class CatalogError(ValueError):
    pass


_OWNER_KINDS = {"component", "api", "resource", "system", "domain"}
_ALLOWED_LIFECYCLES = {"proposed", "experimental", "active", "deprecated", "retired"}


@dataclass(frozen=True)
class Catalog:
    entities: Mapping[str, Entity]

    @classmethod
    def from_records(cls, records: Iterable[Mapping[str, Any]]) -> "Catalog":
        result: dict[str, Entity] = {}
        for record in records:
            ref = entity_ref(str(record["kind"]), str(record.get("namespace", "default")), str(record["name"]))
            if ref in result:
                raise CatalogError(f"duplicate-entity:{ref}")
            known = {"kind","namespace","name","title","owner","lifecycle","system","providesApis","consumesApis","dependsOn"}
            attrs = {k:v for k,v in record.items() if k not in known}
            result[ref] = Entity(
                kind=str(record["kind"]).lower(), namespace=str(record.get("namespace", "default")),
                name=str(record["name"]), title=str(record.get("title", record["name"])),
                owner=record.get("owner"), lifecycle=str(record.get("lifecycle", "active")),
                system=record.get("system"), provides_apis=tuple(record.get("providesApis", ())),
                consumes_apis=tuple(record.get("consumesApis", ())), depends_on=tuple(record.get("dependsOn", ())),
                attributes=attrs,
            )
        catalog = cls(result)
        catalog.validate()
        return catalog

    def get(self, ref: str) -> Entity:
        try:
            return self.entities[ref]
        except KeyError as exc:
            raise CatalogError(f"unknown-entity:{ref}") from exc

    def validate(self) -> None:
        for ref, entity in self.entities.items():
            if entity.lifecycle not in _ALLOWED_LIFECYCLES:
                raise CatalogError(f"invalid-lifecycle:{ref}")
            if entity.kind in _OWNER_KINDS:
                if not entity.owner:
                    raise CatalogError(f"missing-owner:{ref}")
                parse_ref(entity.owner)
                if entity.owner not in self.entities:
                    raise CatalogError(f"unknown-owner:{ref}:{entity.owner}")
                if self.entities[entity.owner].kind != "group":
                    raise CatalogError(f"owner-not-group:{ref}")
            if entity.kind in {"component", "api", "resource"}:
                if not entity.system:
                    raise CatalogError(f"missing-system:{ref}")
                if entity.system not in self.entities or self.entities[entity.system].kind != "system":
                    raise CatalogError(f"invalid-system:{ref}")
            for target in (*entity.provides_apis, *entity.consumes_apis, *entity.depends_on):
                parse_ref(target)
                if target not in self.entities:
                    raise CatalogError(f"unknown-relation:{ref}:{target}")
        implemented: dict[str, int] = {ref:0 for ref,e in self.entities.items() if e.kind == "api"}
        for entity in self.entities.values():
            if entity.kind == "component":
                for api_ref in entity.provides_apis:
                    if self.entities[api_ref].kind != "api":
                        raise CatalogError(f"provides-non-api:{api_ref}")
                    implemented[api_ref] += 1
        for api_ref, count in implemented.items():
            # Capability records without standalone definitions still require an owner component.
            if count == 0:
                raise CatalogError(f"orphan-api:{api_ref}")

    def owner_of(self, ref: str) -> str:
        owner = self.get(ref).owner
        if owner is None:
            raise CatalogError(f"entity-has-no-owner:{ref}")
        return owner

    def api_inventory(self) -> list[tuple[str, Entity]]:
        return sorted(((ref, e) for ref,e in self.entities.items() if e.kind == "api"), key=lambda x:x[0])

    def consumers_of(self, api_ref: str) -> tuple[str, ...]:
        return tuple(sorted(ref for ref,e in self.entities.items() if api_ref in e.consumes_apis))

    def dependency_edges(self) -> tuple[tuple[str,str], ...]:
        edges: list[tuple[str,str]] = []
        for ref, entity in self.entities.items():
            for target in (*entity.consumes_apis, *entity.depends_on):
                edges.append((ref,target))
        return tuple(sorted(edges))
