# Practice Map

Use this page when you want the shortest route from a Deep Dive Make module to a local
exercise, proof loop, and capstone follow-up.

## Module practice surfaces

| Module | Primary practice surface | Main proof loop | Best capstone follow-up |
| --- | --- | --- | --- |
| 01 | tiny truthful build | `make --trace all`, then `make -q all` | inspect the capstone `Makefile` after local convergence is clear |
| 02 | scaling simulator and race repros | compare serial and parallel builds | inspect repros and object discovery surfaces |
| 03 | production build loop | `make selftest` or equivalent | compare with `capstone/tests/run.sh` |
| 04 | precedence and semantics lab | `make -n`, `make --trace`, `make -p` | inspect public target surfaces and diagnostics |
| 05 | hardened build review | convergence, trace count, and portability checks | inspect contract and stamp boundaries |
| 06 | generator playground | trace one generated boundary through the graph | inspect scripts and modeled inputs together |
| 07 | layered repository review | `make help`, `make -p` | inspect the `mk/*.mk` ownership split |
| 08 | release surface review | `make dist`, `make install`, and artifact inspection | inspect package and attestation boundaries |
| 09 | incident diagnosis | follow the incident ladder from preview to repro | compare with capstone incident evidence |
| 10 | written repository review | review rubric plus proof commands | use the capstone as the final stewardship specimen |

## Reusable proof loops

- truth loop: `make --trace all`, `make all`, `make -q all`
- concurrency loop: compare clean serial and parallel builds
- diagnostics loop: `make -n <target>`, `make --trace <target>`, `make -p`
