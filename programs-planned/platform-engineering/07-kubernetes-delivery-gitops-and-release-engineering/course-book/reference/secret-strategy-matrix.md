# Reference — Secret strategy matrix

Encrypted Git provides versioned ciphertext but concentrates decryption authority. External secret controllers separate value authority but add a controller and provider dependency. Runtime retrieval avoids Kubernetes Secret persistence but moves availability and caching into the workload.

Evaluate plaintext locations, key authority, tenant scope, rotation, revocation, audit, recovery, and workload reload behavior. No strategy is universally best.

## Extended reader notes

Compare secret lanes by where plaintext exists, which identity retrieves or decrypts it, how versions are represented, how outages behave, how tenants are separated, and how recovery works.

SOPS stores encrypted values in Git and requires decryption identity in the delivery path. External Secrets stores references in Git and reads plaintext from an external authority. CSI secret drivers can project values without creating a persistent Kubernetes Secret, but application reload and node/plugin trust change. Sealed-secret-style controllers move decryption into the cluster and require careful key backup and rotation.

No lane completes rotation alone. Evidence must show source version, materialized target, workload adoption, and predecessor revocation. Avoid placing a cluster-wide decryption key, repository write credential, and broad Secret access in one controller identity.
