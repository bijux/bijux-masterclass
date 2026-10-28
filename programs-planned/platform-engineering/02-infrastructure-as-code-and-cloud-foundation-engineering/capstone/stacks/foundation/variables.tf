variable "region" {
  description = "AWS region for the Atlas foundation."
  type        = string
}

variable "environment" {
  description = "Foundation environment name."
  type        = string
}

variable "owner" {
  description = "Accountable platform owner."
  type        = string
}

variable "cost_center" {
  description = "Cost-allocation identifier."
  type        = string
}

variable "vpc_cidr" {
  description = "IPv4 CIDR allocated to the Atlas VPC."
  type        = string
  default     = "10.64.0.0/16"
}

variable "availability_zone_names_by_id" {
  description = "Map from stable availability-zone IDs to account-local names."
  type        = map(string)
}

variable "account_id" {
  description = "Expected target AWS account; planning fails on mismatch."
  type        = string

  validation {
    condition     = can(regex("^[0-9]{12}$", var.account_id))
    error_message = "account_id must be a 12-digit AWS account identifier."
  }
}

variable "backup_bucket_name" {
  description = "Globally unique foundation-owned Atlas backup bucket name."
  type        = string
}

variable "audit_enabled" {
  description = "Enable the account-local CloudTrail reference lane."
  type        = bool
  default     = true
}

variable "nat_mode" {
  description = "IPv4 egress profile: none, single, or per-az."
  type        = string
  default     = "none"

  validation {
    condition     = contains(["none", "single", "per-az"], var.nat_mode)
    error_message = "nat_mode must be none, single, or per-az."
  }
}
