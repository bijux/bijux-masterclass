variable "region" {
  description = "AWS region that owns the state foundation."
  type        = string
}

variable "state_bucket_name" {
  description = "Globally unique S3 bucket name for OpenTofu state."
  type        = string

  validation {
    condition     = length(var.state_bucket_name) >= 3 && length(var.state_bucket_name) <= 63
    error_message = "state_bucket_name must be a valid-length S3 bucket name."
  }
}

variable "owner" {
  description = "Accountable owner recorded on state resources."
  type        = string
}

variable "recovery_role_arns" {
  description = "Roles permitted to recover state and decrypt state objects."
  type        = set(string)
  default     = []
}

variable "tags" {
  description = "Additional governed tags."
  type        = map(string)
  default     = {}
}
