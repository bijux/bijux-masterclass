# Guide — collect defensible TLS evidence

A TLS result must answer both confidentiality and identity questions.

## Required fields

Record:

- transport address;
- SNI name;
- expected hostname;
- certificate subject alternative names;
- issuer chain and trust root;
- validity interval and test clock;
- key usage and extended key usage;
- negotiated TLS version, cipher, and ALPN;
- verification result;
- HTTP authority after termination;
- rotation generation or certificate digest.

## Positive and negative controls

Positive: connect to the intended address while verifying the logical hostname and approved CA.

Negative controls:

- wrong hostname;
- untrusted CA;
- expired or not-yet-valid fixture where available;
- wrong HTTP authority after successful TLS;
- missing backend trust policy for re-encryption.

Never use disabled verification as evidence that TLS identity works.

## Gateway-specific questions

- Who owns the listener and certificate reference?
- Does the controller report the reference resolved?
- Is TLS terminated, passed through, or re-encrypted?
- Which headers are replaced at the trusted edge?
- How does certificate rotation overlap work?
- Which connections survive or drain during rotation?

The repository’s private keys are public course fixtures. They establish no real secrecy and must not be deployed.
