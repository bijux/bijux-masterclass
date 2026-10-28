output "instance_profile_name" {
  description = "Instance profile consumed by the workload module."
  value       = aws_iam_instance_profile.runtime.name
}

output "runtime_role_arn" {
  description = "Runtime workload identity for policy review."
  value       = aws_iam_role.runtime.arn
}

output "workload_kms_key_arn" {
  description = "KMS key protecting Atlas workload data."
  value       = aws_kms_key.workload.arn
}
