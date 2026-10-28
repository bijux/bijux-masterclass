from atlas_net.gateway import attach, select_route
from atlas_net.models import HttpMatch, HttpRoute, Listener
from common import emit, record

listener = Listener(
    "https",
    "atlas.example.invalid",
    443,
    "HTTPS",
    "atlas-cert",
    frozenset({"atlas-system"}),
)
good = HttpRoute(
    "atlas",
    "atlas-system",
    "atlas-gateway",
    "https",
    ("atlas.example.invalid",),
    (HttpMatch(path="/"),),
    "atlas-system",
    "atlas-api",
    8080,
)
bad = HttpRoute(
    "evil",
    "tenant-b",
    "atlas-gateway",
    "https",
    ("atlas.example.invalid",),
    (HttpMatch(path="/"),),
    "tenant-b",
    "evil",
    8080,
)
emit(
    "module-07-gateway.json",
    {
        "goodAttachment": record(attach(listener, good, [])),
        "badAttachment": record(attach(listener, bad, [])),
        "selection": record(
            select_route(
                [good, bad],
                listener,
                host="atlas.example.invalid",
                path="/api",
                method="GET",
                headers={},
                grants=[],
            )
        ),
    },
)
