# Atlas Cloud Foundation Architecture

## Ownership

The bootstrap root owns the state bucket and state KMS key. The foundation
root owns the VPC, subnet/route topology, account-local audit path, Atlas
runtime role, workload KMS key, and backup bucket. The workload root owns the
replaceable host, data volume, target registration, and optional edge.

The roots do not share one state. The workload root receives a narrow,
manifested foundation contract. It does not read every foundation output or
consume sensitive state values.

## Deliberate limits

The executable baseline uses one AWS account and one Atlas host. It therefore
does not establish:

- independent organizational log-archive authority;
- multi-zone application availability;
- regional disaster recovery;
- managed database behavior;
- production workload capacity.

The design artifacts show the intended multi-account model, but the release
claim remains bounded to the evidence actually executed.
