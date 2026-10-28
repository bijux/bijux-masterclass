from atlas_net.locality import choose
from atlas_net.models import Endpoint, Service
from common import emit, record

service = Service(
    "atlas-api",
    "atlas-system",
    8080,
    8080,
    ("10.96.0.10", "fd00:10:96::10"),
)
endpoints = (
    Endpoint(
        "10.244.2.10",
        8080,
        "api-b",
        "node-b",
        "zone-b",
        family="IPv4",
    ),
    Endpoint(
        "fd00:10:244:2::10",
        8080,
        "api-b6",
        "node-b",
        "zone-b",
        family="IPv6",
    ),
)
results = {}
for family in ("IPv4", "IPv6"):
    for mode in ("prefer-local", "hard-local", "cluster"):
        results[f"{family}-{mode}"] = record(
            choose(
                service,
                endpoints,
                client_node="node-a",
                client_zone="zone-a",
                client_key="client",
                family=family,
                mode=mode,
            )
        )
emit("module-06-locality.json", results)
