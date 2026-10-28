from __future__ import annotations

from dataclasses import dataclass
from ipaddress import ip_network, ip_address, IPv4Network, IPv6Network
from typing import Any


class NetworkError(ValueError):
    pass


Network = IPv4Network | IPv6Network


def subnet_from_slot(vpc_cidr: str, new_prefix: int, slot: int) -> str:
    vpc = ip_network(vpc_cidr)
    if new_prefix < vpc.prefixlen:
        raise NetworkError("new prefix cannot be shorter than VPC prefix")
    subnets = vpc.subnets(new_prefix=new_prefix)
    for index, subnet in enumerate(subnets):
        if index == slot:
            return str(subnet)
    raise NetworkError("subnet slot is outside the VPC address space")


def validate_network_plan(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        vpc = ip_network(plan["vpcCidr"])
    except Exception as exc:
        return [f"invalid VPC CIDR: {exc}"]
    networks: list[tuple[str, Network]] = []
    names: set[str] = set()
    for row in plan.get("subnets", []):
        name = str(row.get("name", ""))
        if not name:
            errors.append("subnet name is required")
            continue
        if name in names:
            errors.append(f"duplicate subnet name: {name}")
        names.add(name)
        try:
            subnet = ip_network(row["cidr"])
        except Exception as exc:
            errors.append(f"invalid subnet {name}: {exc}")
            continue
        if not subnet.subnet_of(vpc):
            errors.append(f"subnet {name} is outside the VPC")
        for other_name, other in networks:
            if subnet.overlaps(other):
                errors.append(f"subnets overlap: {other_name} and {name}")
        networks.append((name, subnet))
        if row.get("tier") == "data" and row.get("defaultRoute") in {"igw", "nat"}:
            errors.append(f"data subnet {name} must not have direct internet default route")
    azs = {row.get("azId") for row in plan.get("subnets", []) if row.get("azId")}
    if len(azs) < int(plan.get("requiredAvailabilityZones", 1)):
        errors.append("network plan does not cover required availability zones")
    return errors


@dataclass(frozen=True)
class Route:
    destination: Network
    target: str
    source: str


def select_route(address: str, routes: list[dict[str, str]]) -> Route:
    ip = ip_address(address)
    candidates: list[Route] = []
    for row in routes:
        destination = ip_network(row["destination"])
        if ip.version == destination.version and ip in destination:
            candidates.append(Route(destination, row["target"], row.get("source", "route-table")))
    if not candidates:
        raise NetworkError(f"no route for {address}")
    return sorted(candidates, key=lambda route: route.destination.prefixlen, reverse=True)[0]


def trace_path(plan: dict[str, Any], *, source_subnet: str, destination_ip: str) -> dict[str, Any]:
    subnet = next((row for row in plan.get("subnets", []) if row.get("name") == source_subnet), None)
    if subnet is None:
        raise NetworkError(f"unknown source subnet: {source_subnet}")
    route = select_route(destination_ip, subnet.get("routes", []))
    allowed = route.target not in {"blackhole", "none"}
    if subnet.get("tier") == "data" and route.target in {"igw", "nat"}:
        allowed = False
    return {
        "sourceSubnet": source_subnet,
        "destination": destination_ip,
        "matchedRoute": str(route.destination),
        "target": route.target,
        "allowed": allowed,
    }
