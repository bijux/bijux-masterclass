from __future__ import annotations

from ipaddress import ip_address, ip_network

from .models import Route


class RouteError(ValueError):
    pass


def select_route(
    destination: str,
    routes: list[Route],
    table: int = 254,
) -> tuple[Route, list[Route]]:
    """Select by longest prefix, then lower metric, within one route table."""

    destination_ip = ip_address(destination)
    candidates: list[tuple[int, int, Route]] = []
    visible: list[Route] = []

    for route in routes:
        if route.table != table:
            continue
        network = ip_network(route.prefix, strict=False)
        if destination_ip.version != network.version or destination_ip not in network:
            continue
        visible.append(route)
        candidates.append((network.prefixlen, -route.metric, route))

    if not candidates:
        raise RouteError(f"no route to {destination} in table {table}")

    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    visible.sort(
        key=lambda route: ip_network(route.prefix, strict=False).prefixlen,
        reverse=True,
    )
    return candidates[0][2], visible


def validate_non_overlapping(prefixes: dict[str, list[str]]) -> list[str]:
    """Return every same-family overlap across named address domains."""

    errors: list[str] = []
    items = [
        (domain, ip_network(value, strict=False))
        for domain, values in prefixes.items()
        for value in values
    ]
    for index, (left_domain, left_network) in enumerate(items):
        for right_domain, right_network in items[index + 1 :]:
            if (
                left_network.version == right_network.version
                and left_network.overlaps(right_network)
            ):
                errors.append(
                    f"{left_domain}:{left_network} overlaps "
                    f"{right_domain}:{right_network}"
                )
    return errors
