# State Bootstrap

This root creates the state bucket and KMS key before other stacks can use the
S3 backend. It intentionally uses local state during first creation. After the
bucket is created, preserve the bootstrap state under the documented recovery
procedure; do not point the bootstrap root at the bucket it is responsible for
deleting/protecting without an explicit migration.

Example (sandbox only):

```bash
tofu init
tofu plan -out bootstrap.tfplan
tofu apply bootstrap.tfplan
```
