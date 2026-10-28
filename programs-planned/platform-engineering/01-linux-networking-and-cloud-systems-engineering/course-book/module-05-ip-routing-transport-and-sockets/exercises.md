# Exercises — Module 05: IP, Routing, Transport, and Sockets

Complete these before opening the worked answers. Each response must name the mechanism, failure boundary, and decisive evidence where relevant.

## Exercise 1 — Wildcard listener

Compare `127.0.0.1:8080`, `0.0.0.0:8080`, `[::1]:8080`, and `[::]:8080`.

## Exercise 2 — Route get

Why is `ip route get <destination>` often more useful than reading the default route?

## Exercise 3 — TCP framing

Why can one `recv` return half of one application message or several messages together?

## Exercise 4 — UDP trade-off

Which guarantees must an application add if it needs reliable ordered effects over UDP?

## Exercise 5 — TIME_WAIT

Why is a large TIME_WAIT count not automatically a socket leak?

## Exercise 6 — Timeout phases

A client connects immediately but hangs forever waiting for response bytes. Which timeout was missing?

## Exercise 7 — Loopback edge

Why is loopback a strong default for an API behind a same-host reverse proxy?

## Exercise 8 — IPv6 evidence

What must be checked before claiming an endpoint supports IPv6?

## Exercise 9 — Listen backlog

What does increasing the listen backlog not fix?

## Exercise 10 — NAT identity

Why should an application not authorize a user from the source IP observed after NAT?

## Exercise 11 — Unix socket alternative

When might a Unix-domain socket be preferable between edge and API?

## Exercise 12 — Failure localization

A client receives connection refused. List the likely path state and the first three observations.
