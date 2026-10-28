# Checkpoint 06 — Authorization, Tenancy, and Schema Exposure

Do not continue until every condition is supported by executable or inspected evidence.

- [ ] Root, object, collection, field, and mutation authorization decisions are all explicit and default-deny.
- [ ] Tenant isolation is enforced by source queries or policy inputs, not inferred from parent traversal.
- [ ] Denied protected fields cause zero downstream calls and return only the declared nullable/error behavior.
- [ ] Global IDs, aliases, fragments, node lookup, and search cannot bypass ownership or field policy.
- [ ] Request-scoped loader keys cannot share a protected value across principals or tenants.
- [ ] Lab 06 includes wrong-tenant, missing-permission, field-level denial, and support-context cases with call-count evidence.

**Gate:** run `make module-06-proof`. A green command without the lab report and the listed evidence does not count.
