# Lab — Module 05: IP, Routing, Transport, and Sockets

## Goal

Trace one Atlas connection from client route to listening process and expose the difference between loopback and wildcard bindings.

## Safety boundary

The namespace route requires root and explicit opt-in inside a disposable VM. Do not alter the default route of a remote host.

## Baseline

Start Atlas and capture `ip address`, `ip route`, `ip rule`, `ss -lntp`, and one successful loopback request.

## Hypothesis

The internal API is reachable through loopback by the same host but not through a remote interface; the edge owns external exposure.

## Controlled action

Test the internal API through loopback and the host interface. Run the namespace lab to create two isolated endpoints. Change only a lab listener from loopback to wildcard and observe the new reachable tuples before restoring it.

## Oracle

Listener address and route evidence predict success or refusal; no administrative or worker listener becomes external; IPv4 and IPv6 behavior are recorded separately.

## Evidence

Listener ownership, route selection, namespace address/route tables, successful and failed connection transcripts, and timeout/refusal classification.

## Interpretation

Explain whether the hypothesis was supported, falsified, or remained untested. Distinguish a mechanism result from a production claim and identify the first observation that changed your diagnosis.

## Cleanup

Restore the listener, delete only lab namespaces/veth pairs through the script trap, and confirm no route or namespace remains.

## Completion gate

Explain why firewall policy and listener binding are complementary rather than interchangeable.

Do not progress with an ambiguous cleanup state or an unexplained deviation from the expected oracle.
