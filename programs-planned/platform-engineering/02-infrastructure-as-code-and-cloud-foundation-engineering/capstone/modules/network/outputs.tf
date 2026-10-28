output "vpc_id" {
  description = "VPC identifier owned by this module."
  value       = aws_vpc.this.id
}

output "vpc_cidr" {
  description = "VPC address boundary for policy and composition."
  value       = aws_vpc.this.cidr_block
}

output "subnet_ids" {
  description = "Subnet identifiers keyed by stable semantic identity."
  value       = { for key, subnet in aws_subnet.this : key => subnet.id }
}

output "public_subnet_ids" {
  description = "Public subnet identifiers for edge resources."
  value       = { for key in keys(local.public_subnets) : key => aws_subnet.this[key].id }
}

output "private_subnet_ids" {
  description = "Private subnet identifiers for workload placement."
  value       = { for key in keys(local.private_subnets) : key => aws_subnet.this[key].id }
}

output "data_subnet_ids" {
  description = "Data subnet identifiers; no default internet route is created."
  value       = { for key in keys(local.data_subnets) : key => aws_subnet.this[key].id }
}

output "subnet_az_names" {
  description = "Account-local availability-zone names keyed by subnet identity."
  value = {
    for key, subnet in var.subnets : key => var.availability_zone_names_by_id[subnet.az_id]
  }
}
