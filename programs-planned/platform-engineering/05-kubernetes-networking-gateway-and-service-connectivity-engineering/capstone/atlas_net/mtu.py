from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Encapsulation:
    name: str
    bytes: int


def effective_mtu(
    underlay_mtu: int,
    layers: list[Encapsulation],
    safety: int = 0,
) -> int:
    if underlay_mtu <= 0 or safety < 0:
        raise ValueError("invalid MTU input")
    if any(layer.bytes < 0 for layer in layers):
        raise ValueError("encapsulation overhead cannot be negative")

    result = underlay_mtu - sum(layer.bytes for layer in layers) - safety
    if result < 576:
        raise ValueError("effective MTU is implausibly small")
    return result


def packet_fits(payload_ip_size: int, mtu: int) -> bool:
    return 0 < payload_ip_size <= mtu
