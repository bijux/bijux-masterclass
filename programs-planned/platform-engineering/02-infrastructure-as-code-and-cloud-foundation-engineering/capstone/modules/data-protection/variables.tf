variable "name" {
  description = "Stable Atlas data-resource prefix."
  type        = string
}

variable "availability_zone" {
  description = "Availability zone of the workload that attaches the EBS volume."
  type        = string
}

variable "volume_size_gib" {
  description = "Capacity of the durable Atlas data volume."
  type        = number
  default     = 20

  validation {
    condition     = var.volume_size_gib >= 1
    error_message = "volume_size_gib must be at least 1 GiB."
  }
}

variable "kms_key_arn" {
  description = "Foundation-owned KMS key used for EBS encryption."
  type        = string
}


variable "tags" {
  description = "Governed inventory and cost-allocation tags."
  type        = map(string)
}
