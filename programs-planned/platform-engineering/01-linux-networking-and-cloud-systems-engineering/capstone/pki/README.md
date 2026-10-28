# Local PKI Fixture — Not a Deployable Secret Set

This directory contains a deliberately checked-in local certificate authority and server key used only by the dependency-light Atlas Host Runtime tour.

The fixture exists so that learners can exercise trust-store loading, SNI, hostname verification, certificate inspection, and TLS failure behavior without an external certificate service. The private keys are public course material. They provide **no secrecy or identity assurance** outside this repository.

A real environment must generate independent keys, protect them with an appropriate secret or key-management boundary, define renewal and revocation ownership, and prove certificate deployment and rotation in that environment. Never reuse these keys or certificates for another host, network, or course deployment.
