# Standards and Reference Profile

Snapshot date: **2026-08-09**.

## Executable reference versions

- OpenTofu 1.12.5
- AWS provider 6.58.0
- Python 3.12 or newer

## Normative and primary references

- [OpenTofu language and state documentation](https://opentofu.org/docs/)
- [OpenTofu state and plan encryption](https://opentofu.org/docs/language/state/encryption/)
- [OpenTofu S3 backend](https://opentofu.org/docs/language/settings/backends/s3/)
- [AWS Organizations multi-account best practices](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices.html)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [Amazon VPC documentation](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [IAM roles for EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)
- [EC2 instance metadata options](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-options.html)
- [Application Load Balancer target health](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)

## Course policies

These are narrower than what the tools may permit:

- no root-account use;
- no long-lived cloud keys in configuration or state;
- no default apply target;
- one state writer at a time;
- versioned remote state with recoverable locking;
- explicit region and account allowlists;
- flat module composition;
- destructive change requires explicit approval;
- imported resources require complete configuration before adoption;
- manual state mutation is an incident procedure, not routine workflow;
- a successful apply is followed by data-plane validation;
- every real-cloud lab ends with a cleanup or retained-resource ownership record.
