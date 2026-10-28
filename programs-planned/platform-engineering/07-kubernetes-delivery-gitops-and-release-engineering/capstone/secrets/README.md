# Secret delivery lanes

The External Secrets lane keeps values outside Git and reconciles a runtime Secret from a named source. The SOPS lane stores encrypted values in Git and requires a decryption identity at reconciliation time. Neither lane makes secret adoption by the workload automatic: the release evidence must show which version was projected, when the application adopted it, and whether the predecessor was revoked safely.

All values in this directory are synthetic fixtures. They provide no confidentiality.
