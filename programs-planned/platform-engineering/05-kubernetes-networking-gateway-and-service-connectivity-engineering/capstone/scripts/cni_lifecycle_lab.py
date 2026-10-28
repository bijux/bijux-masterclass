from atlas_net.cni import CNIState

from common import emit


state = CNIState("10.244.1.0/29")
state.add(
    network="atlas",
    attachment_id="old",
    container_id="c1",
    pod_uid="api:uid-old",
    interface="eth0",
    generation=1,
)
state.add(
    network="atlas",
    attachment_id="new",
    container_id="c2",
    pod_uid="api:uid-new",
    interface="eth0",
    generation=2,
)

before = state.snapshot()
removed = state.gc({("new", 2)})

# DEL is deliberately replayed to prove idempotent cleanup.
state.delete("old")
state.delete("old")

emit(
    "module-02-cni.json",
    {
        "before": before,
        "removed": removed,
        "after": state.snapshot(),
        "actions": state.actions,
    },
)
