output "workload_release" {
  description = "Identifiers used by post-apply and replacement evidence."
  value = {
    launch_template_id      = module.workload.launch_template_id
    launch_template_version = module.workload.launch_template_latest_version
    instance_id             = module.workload.instance_id
    data_volume_id          = module.data_protection.data_volume_id
    backup_bucket_arn       = var.foundation_contract.backup_bucket_arn
    edge_dns_name           = module.edge.dns_name
    target_group_arn        = module.edge.target_group_arn
  }
}
