# Course 6 — Node.js Networking, HTTP, and Service Architecture

Networking exposes assumptions that local code can postpone. A function call has one caller and one callee in one process. A network operation crosses address resolution, operating-system queues, partial delivery, peer-controlled timing, protocol parsing, admission policy, and independent failure. A request can time out after the server commits. A connection can close after carrying a complete message. A valid TLS certificate can identify the wrong host. An HTTP response can be syntactically complete but semantically stale. A service can stop accepting traffic while hundreds of accepted operations remain unfinished.

This course makes those distinctions explicit.

## The course thesis

A network service is a collection of protocols, not a listening socket.

Each protocol needs:

1. **a representation** — bytes, frames, headers, fields, or events;
2. **a state machine** — which messages are legal now;
3. **an authority** — which component may commit a state transition;
4. **a capacity model** — what can accumulate and how much;
5. **a time model** — one deadline, idle policy, heartbeat, or retry budget;
6. **a failure model** — malformed input, overload, timeout, disconnect, peer failure, internal failure;
7. **a terminal model** — completion, rejection, cancellation, close, abort, and join;
8. **evidence** — tests and observations that distinguish the intended contract from a plausible but incorrect implementation.

The course repeatedly asks you to separate three layers:

```text
transport fact
    from
protocol fact
    from
product fact
```

TCP delivers an ordered byte stream; it does not preserve application messages. HTTP defines methods and responses; it does not define your domain's idempotency semantics. TLS authenticates an identity under a trust policy; it does not prove that the peer is authorized to perform a business operation.

## The ten-module progression

The first three modules work below HTTP. You learn how names become address candidates, how TCP connections carry bounded frames, and why UDP requires correlation and duplicate policy.

Modules 54 and 55 construct the server-side HTTP boundary. Module 56 reverses perspective and treats the client as a resource-owning subsystem with pooling, deadlines, redirects, response limits, and retry policy.

Modules 57 and 58 add secure transport identity and multiplexed sessions. Module 59 handles long-lived HTTP delivery through server-sent events. Module 60 combines all authorities and asks whether the complete product can admit, reject, drain, abort, and terminate honestly.

## What “complete” means here

Completion is not reading every page. You must be able to:

- draw the state machine before implementing it;
- identify every queue and retained structure;
- name the owner of every socket, agent, session, subscription, timer, and shutdown obligation;
- predict how arbitrary chunking affects a protocol parser;
- distinguish deadline expiry from rollback;
- define when retry is safe and when commit is ambiguous;
- preserve causal error information without exposing peer-controlled secrets;
- give one terminal outcome to every accepted operation;
- demonstrate deterministic product output despite nondeterministic network schedules;
- implement the final independent change without bypassing validation or lifecycle contracts.

## Reader discipline

Do not begin with the reference implementation. The reference is one defensible design, not the definition of truth. Your first obligation is to state the public contract and write tests that would fail under the shortcuts named in the laboratory brief.

When the observed runtime differs from your prediction, classify the difference:

- JavaScript scheduling;
- Node API behavior;
- operating-system behavior;
- protocol semantics;
- product policy;
- test-environment assumption.

That classification prevents “Node did something strange” from replacing technical explanation.

## Course artifacts

- [Learning outcomes](outcomes.md)
- [Ten-day study plan](study-plan.md)
- [Networking reference desk](reference.md)
- [Final review](final-review.md)
- [Reasoned final-review solutions](final-review-solutions.md)
- [ServiceWire engineering guide](capstone.md)

Begin with [Module 51](module-51-network-boundaries-addresses-dns-sockets-and-time/index.md).
