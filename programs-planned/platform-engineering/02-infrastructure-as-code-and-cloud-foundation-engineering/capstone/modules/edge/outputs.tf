output "edge_security_group_id" {
  description = "Public edge security group identity."
  value       = try(aws_security_group.edge[0].id, null)
}

output "dns_name" {
  description = "Load-balancer DNS name when the optional edge is enabled."
  value       = try(aws_lb.atlas[0].dns_name, null)
}

output "target_group_arn" {
  description = "Target group used by post-apply health verification."
  value       = try(aws_lb_target_group.atlas[0].arn, null)
}
