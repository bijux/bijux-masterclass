# Egress destination classification

Classify every resolved and connected address:

- public routable;
- private;
- loopback;
- link-local;
- multicast;
- unspecified;
- reserved/documentation;
- metadata-service range;
- explicitly owned internal range.

An allowlisted hostname does not override address policy. Resolve all candidates, connect under a deadline, verify the actual peer, validate TLS, and repeat policy on redirects.

Private or documentation ranges can be permitted only through an explicit course/environment exception. Record which resolver and proxy path enforced the decision.
