from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DNSAnswer:
    rcode: str
    values: tuple[str, ...]
    ttl: int


class DNSAuthority:
    def __init__(self) -> None:
        self.records: dict[tuple[str, str], DNSAnswer] = {}

    def set(
        self,
        name: str,
        record_type: str,
        values: list[str],
        ttl: int = 30,
    ) -> None:
        self.records[(name.rstrip("."), record_type)] = DNSAnswer(
            "NOERROR",
            tuple(values),
            ttl,
        )

    def delete(self, name: str, record_type: str) -> None:
        self.records.pop((name.rstrip("."), record_type), None)

    def query(self, name: str, record_type: str) -> DNSAnswer:
        return self.records.get(
            (name.rstrip("."), record_type),
            DNSAnswer("NXDOMAIN", (), 10),
        )


class DNSCache:
    def __init__(self, authority: DNSAuthority) -> None:
        self.authority = authority
        self.entries: dict[tuple[str, str], tuple[int, DNSAnswer]] = {}
        self.trace: list[dict[str, object]] = []

    def query(self, name: str, record_type: str, now: int) -> DNSAnswer:
        key = (name.rstrip("."), record_type)
        cached = self.entries.get(key)
        if cached and now < cached[0]:
            self.trace.append(
                {
                    "name": key[0],
                    "type": record_type,
                    "source": "cache",
                    "expires": cached[0],
                    "rcode": cached[1].rcode,
                }
            )
            return cached[1]

        answer = self.authority.query(*key)
        expires = now + answer.ttl
        self.entries[key] = (expires, answer)
        self.trace.append(
            {
                "name": key[0],
                "type": record_type,
                "source": "authority",
                "expires": expires,
                "rcode": answer.rcode,
            }
        )
        return answer


def expand_name(name: str, search: list[str], ndots: int) -> list[str]:
    """Return candidate names in the course resolver profile's query order."""

    if name.endswith("."):
        return [name[:-1]]

    candidates: list[str] = []
    if name.count(".") >= ndots:
        candidates.append(name)
    candidates.extend(f"{name}.{suffix}" for suffix in search)
    if name not in candidates:
        candidates.append(name)
    return candidates
