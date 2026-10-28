output "audit_bucket_arn" {
  description = "Account-local audit destination; not equivalent to an independent log-archive account."
  value       = aws_s3_bucket.audit.arn
}

output "audit_kms_key_arn" {
  description = "KMS key used by the account-local audit trail."
  value       = aws_kms_key.audit.arn
}
