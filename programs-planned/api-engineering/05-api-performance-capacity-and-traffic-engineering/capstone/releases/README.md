# Performance release fixtures

The baseline and four candidates exercise every decision state:

- `accepted-candidate` is comparable, correct, fully observed, and within all
  versioned metric policies;
- `rejected-faster-but-wrong` demonstrates gate precedence;
- `inconclusive-environment-mismatch` refuses an unsupported comparison;
- `rejected-regression` is correct but exceeds latency, throughput, and memory
  policy.

A failed candidate never replaces the baseline. The release proof evaluates the
same envelopes in Python and TypeScript and compares the statuses.
