output "foundation_contract" {
  description = "Narrow published contract consumed by the workload root."
  value = {
    vpc_id                    = module.network.vpc_id
    vpc_cidr                  = module.network.vpc_cidr
    public_subnet_ids         = module.network.public_subnet_ids
    private_subnet_ids        = module.network.private_subnet_ids
    private_subnet_az_names   = {
      for key, az_name in module.network.subnet_az_names : key => az_name
      if contains(keys(module.network.private_subnet_ids), key)
    }
    instance_profile_name     = module.identity.instance_profile_name
    runtime_role_arn          = module.identity.runtime_role_arn
    workload_kms_key_arn      = module.identity.workload_kms_key_arn
    audit_bucket_arn          = module.audit.audit_bucket_arn
    backup_bucket_arn         = aws_s3_bucket.backup.arn
    governed_tags             = module.naming.tags
  }
}
