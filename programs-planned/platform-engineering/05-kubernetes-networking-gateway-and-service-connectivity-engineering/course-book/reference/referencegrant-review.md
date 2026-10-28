# ReferenceGrant review

A ReferenceGrant is created in the target namespace. Review:

- source API group;
- source kind;
- source namespace;
- target API group;
- target kind;
- optional target name;
- business and operational reason;
- owner and expiry if temporary.

Avoid grants that authorize all Route namespaces or all Services without a documented platform contract. The grant permits the reference; NetworkPolicy, workload identity, and application authorization still govern actual use.

Negative evidence should show that the same reference fails without the grant and that an unrelated source namespace remains unauthorized.
