variable "name" {
  description = "Stable Atlas workload identity prefix."
  type        = string
}

variable "region" {
  description = "AWS region containing Atlas runtime dependencies."
  type        = string
}

variable "account_id" {
  description = "AWS account that owns the workload role and resources."
  type        = string

  validation {
    condition     = can(regex("^[0-9]{12}$", var.account_id))
    error_message = "account_id must be a 12-digit AWS account identifier."
  }
}

variable "environment" {
  description = "Environment represented by this workload identity."
  type        = string
}

variable "config_parameter_prefix" {
  description = "SSM Parameter Store path, without a leading slash, readable by Atlas."
  type        = string
}

variable "secret_prefix" {
  description = "Secrets Manager name prefix readable by Atlas."
  type        = string
}

variable "backup_bucket_arn" {
  description = "Exact foundation-owned bucket ARN receiving Atlas result backups."
  type        = string
}

variable "tags" {
  description = "Governed inventory and cost-allocation tags."
  type        = map(string)
}
