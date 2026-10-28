# Exercises — Module 02: Identity, Permissions, Capabilities, and Service Supervision

Complete these before opening the worked answers. Each response must name the mechanism, failure boundary, and decisive evidence where relevant.

## Exercise 1 — Directory versus file write

A user cannot modify a file but can delete it. Explain the permission model.

## Exercise 2 — Umask reasoning

A process calls `open` requesting mode `0666` under umask `0027`. What mode is normally created and what does this not guarantee?

## Exercise 3 — Why not root

Give three distinct ways running Atlas as root increases impact beyond what the workload needs.

## Exercise 4 — Capability choice

The edge listens on port 8443. Should it receive `CAP_NET_BIND_SERVICE`? Defend the answer.

## Exercise 5 — After versus Requires

Explain why `After=network.target` does not mean the network is usable and why `Requires=` would not prove it either.

## Exercise 6 — Restart policy

A service exits code 0 immediately because configuration is missing. Why may `Restart=on-failure` leave it down without obvious recovery?

## Exercise 7 — Writable code

Why is `/opt/atlas` writable by `atlas-api` a persistence risk even if the service cannot edit its unit?

## Exercise 8 — Secrets in environment

Why is a systemd environment variable not automatically an appropriate secret-delivery channel?

## Exercise 9 — Readiness ownership

Who should decide Atlas readiness: systemd, the reverse proxy, or the application?

## Exercise 10 — ACL trade-off

When is an ACL justified instead of adding another shared Unix group?

## Exercise 11 — NoNewPrivileges

What does `NoNewPrivileges=yes` prevent and what does it not prevent?

## Exercise 12 — Authority proof

Design an evidence set proving that the API can write its spool request path but cannot write code or TLS keys.
