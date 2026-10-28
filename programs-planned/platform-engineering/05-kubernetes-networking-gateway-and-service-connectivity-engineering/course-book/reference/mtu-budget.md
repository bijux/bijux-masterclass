# MTU budget

Calculate the inner-packet budget:

```text
underlay MTU
- overlay headers
- encryption headers
- additional encapsulation
= safe inner MTU
```

The exact overhead depends on protocol, address family, options, and implementation. Verify the configured Pod interface rather than copying a generic number.

Evidence for a suspected black hole:

- successful small request and failed larger request;
- payload-size boundary;
- interface and path MTUs;
- outer/inner packet sizes;
- ICMP fragmentation-needed or Packet Too Big behavior;
- TCP retransmissions and MSS;
- same-Node versus cross-Node comparison;
- IPv4 versus IPv6 comparison.

Lowering MTU everywhere can hide the failed control message or wrong tunnel budget. Fix the owned path and retain a regression around the observed boundary.
