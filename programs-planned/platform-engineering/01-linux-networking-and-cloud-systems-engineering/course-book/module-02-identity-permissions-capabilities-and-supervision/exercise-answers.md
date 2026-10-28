# Worked Answers — Module 02: Identity, Permissions, Capabilities, and Service Supervision

These answers demonstrate reasoning. Equivalent answers are valid when they preserve the same mechanism and evidence boundary.

## Exercise 1 — Directory versus file write

Changing file contents requires write permission on the file. Removing its name modifies the containing directory, so directory write plus traversal permission can permit deletion even when the file is read-only. Sticky-directory rules and immutable attributes can add constraints. Diagnose with `namei -l` across the complete path, not only `ls -l` on the file.

## Exercise 2 — Umask reasoning

The umask clears group-write and all other bits, producing `0640` before ACL or filesystem effects. It does not guarantee parent-directory privacy, existing-file mode, secret non-disclosure through descriptors or logs, or correct ownership. Verify the created object and the full path. Treat umask as a creation default, not the complete access policy.

## Exercise 3 — Why not root

A root Atlas process can modify system configuration and service units, read unrelated secrets, change network policy, mount filesystems, alter ownership, and escape intended writable paths. A vulnerability becomes host compromise rather than service-account compromise. The correct model assigns dedicated users and only required path or kernel authority. Root is not needed for loopback listeners or ordinary file-spool access.

## Exercise 4 — Capability choice

No. That capability is relevant to privileged low ports, and 8443 does not require it. Granting the capability adds authority without enabling a requirement. If deployment later binds 443 directly, compare a narrow capability with socket activation or a separate maintained proxy. Verify the effective capability set of the running process rather than leaving a copied unit directive.

## Exercise 5 — After versus Requires

`After=` only orders unit startup relative to another unit. `Requires=` adds a dependency relationship and stop behavior, but the required unit can be active before DNS, routing, or an external endpoint is usable. Application readiness or an explicit network-online mechanism must test the actual prerequisite. Avoid turning vague target names into semantic guarantees.

## Exercise 6 — Restart policy

`on-failure` does not restart a clean exit. If initialization mistakenly reports success, the supervisor believes the unit completed normally. The application must return a non-zero status for failed startup, and the unit type must match whether a persistent service is expected. Verify active state, main PID, and exit result rather than assuming restart policy repairs initialization.

## Exercise 7 — Writable code

The service can replace code or modules that the privileged deployment or supervisor executes on restart. An attacker can persist through process restart and potentially exploit a more privileged execution context. Application release content should be immutable to the service identity. Mutable cache or data belongs in separately owned paths such as `/var/cache` or `/var/lib`.

## Exercise 8 — Secrets in environment

Environment values can be inherited by children, exposed through diagnostics or crash handling, copied into logs, and retained longer than intended. Access depends on operating-system policy and tooling. Secret delivery needs identity, scope, file or credential permissions, rotation, and revocation. Course fixture variables are not production secret management.

## Exercise 9 — Readiness ownership

The application owns semantic checks such as spool writability and worker freshness. The proxy consumes the readiness result for routing. systemd owns process lifecycle and can use application notification, but it cannot infer business prerequisites from PID presence. Keep responsibilities separate: process alive, route eligible, and operation correct are different claims.

## Exercise 10 — ACL trade-off

An ACL is useful when one object needs a specific additional principal or permission that does not align with a stable group. It should have an owner and review path because it is less visible than simple mode/group policy. If many paths require ad hoc ACLs, the service boundary or directory ownership is probably unclear. Verify default ACL inheritance as well as current entries.

## Exercise 11 — NoNewPrivileges

It prevents the process and descendants from gaining additional privilege through exec mechanisms such as set-ID binaries or file capabilities. It does not remove privileges already held, constrain filesystem access by itself, block network calls, or make vulnerable code safe. Combine it with minimal credentials, capabilities, path policy, namespaces, and application controls.

## Exercise 12 — Authority proof

Record effective UID/GID/groups and capabilities from `/proc`, unit properties, `namei -l` for each path, and controlled write attempts as the service identity. The positive test writes and removes a fixture under the authorized state path. Negative tests fail under `/opt/atlas` and `/etc/atlas/tls`. Preserve errors and verify no file appeared. Static modes alone do not prove the running identity.
