# Custom-resource evolution

A CRD creates an API compatibility obligation. Stored objects can outlive a controller release, and clients can depend on fields, defaults, validation, and status reasons.

## Structural schemas

Use typed structural schemas so pruning, defaulting, and subresources behave predictably. Avoid free-form fields unless the data is intentionally opaque. Validation should reject impossible combinations close to admission.

## Version path

An alpha version can change, but change still needs migration evidence. Before serving multiple versions, define storage version, conversion strategy, round-trip expectations, and rollback limits. A conversion webhook becomes a critical availability dependency for reads/writes that need conversion.

## Defaulting

Defaults become part of API behavior. Changing a default affects newly created objects but not necessarily stored objects that already contain old values. Controllers should operate on admitted explicit state, not assume current default code was applied historically.

## Deletion compatibility

New controller versions must understand finalizers and cleanup obligations created by old versions. Removing finalizer support before old objects are gone can deadlock deletion or orphan external resources.
