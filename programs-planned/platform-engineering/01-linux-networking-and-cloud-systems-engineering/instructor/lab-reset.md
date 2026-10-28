# Laboratory Reset and Cleanup

## Dependency-light route

```bash
make clean
pgrep -af 'atlas_host|atlas-api|atlas-worker|atlas-edge' || true
```

Confirm no generated runtime directory, report file, or temporary certificate process remains. Re-run manifest proof.

## Privileged VM route

Before reuse:

- remove `atlas-left` and `atlas-right` namespaces;
- inspect routes, links, mounts, cgroups, nftables tables, and installed units;
- restore the known firewall baseline through console access;
- remove temporary users, groups, certificates, and state;
- reboot when the exercise intentionally tests boot convergence;
- compare against the VM snapshot or rebuild from the declared image.

## Cloud route

List resources by course tag and account/project/subscription. Verify instances, disks, addresses, load balancers, snapshots, DNS records, identities, and temporary policies are deleted or retained intentionally. Record the billing inventory after cleanup.

Never hand the next learner an environment with unexplained residual state.
