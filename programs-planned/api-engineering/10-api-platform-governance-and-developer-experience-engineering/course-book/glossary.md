# Glossary — API Platform, Governance, and Developer Experience Engineering

These terms have precise meanings in Course 10. Use them with the program glossary at `program-book/glossary.md`, which preserves shared meanings across the complete sequence.

## platform product

A maintained internal product that reduces recurring API delivery and consumption work while leaving domain authority with domain owners.

## paved road

A supported, automated route for a recurring task that is easier than bespoke work but allows justified, governed exceptions.

## catalog

A searchable graph of APIs, components, resources, systems, domains, groups, and their relationships.

## entity reference

A canonical, stable identifier used to refer to one catalog entity across metadata, policy, support, and automation.

## API product

A governed interface offered to consumers with an owner, lifecycle, contract releases, documentation, support, and usage evidence.

## owner

The accountable group empowered to decide and support a defined artifact, capability, policy, or business fact.

## registry

A publication system that stores immutable contract or package releases by identity, version, digest, and metadata.

## immutable release

A published version whose bytes and digest never change; corrections require a new version.

## policy as code

Executable, versioned decision logic that evaluates explicit inputs and produces inspectable results rather than relying on undocumented review custom.

## evidence record

A versioned record linking a policy claim to a proof result, environment, owner, freshness, and retained artifact.

## scorecard

A categorical view of required evidence and policy outcomes; blocker failures cannot be hidden by an average score.

## exception

A bounded, approved deviation with owner, reason, compensating control, expiry, and closure path.

## lifecycle

The governed progression of an API product through states such as proposed, experimental, active, deprecated, and retired.

## deprecation

A lifecycle state communicating that consumers must migrate away while the old interface remains supported for a declared period and population.

## retirement

The removal of support and availability after consumer evidence, migration, approval, and operational conditions are satisfied.

## consumer inventory

Evidence identifying who depends on an API version, how they use it, and whether they have completed required migration.

## golden path

A tested template and workflow producing a known set of artifacts, defaults, checks, and ownership metadata for a recurring delivery task.

## sandbox

An isolated, synthetic-data environment for safe learning and integration testing with bounded credentials and resource use.

## SBOM

A software bill of materials listing components and relationships in a build or artifact; it does not by itself prove absence of vulnerabilities.

## provenance

Evidence describing how, where, and from which inputs an artifact was built, with an explicit trust and attestation boundary.

## runtime drift

A difference between approved desired configuration and observed deployed routes, policies, versions, or ownership metadata.

## support routing

The rules that direct a consumer problem to the accountable platform or domain owner with enough context for action.
