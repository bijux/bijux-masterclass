output "state_bucket" {
  description = "State bucket name for backend configuration."
  value       = aws_s3_bucket.state.id
}

output "state_kms_key_arn" {
  description = "KMS key used for server-side state encryption."
  value       = aws_kms_key.state.arn
}

output "backend_config_example" {
  description = "Non-secret values used to initialize an S3 backend."
  value = {
    bucket       = aws_s3_bucket.state.id
    region       = var.region
    use_lockfile = true
    encrypt      = true
    kms_key_id   = aws_kms_key.state.arn
  }
}
