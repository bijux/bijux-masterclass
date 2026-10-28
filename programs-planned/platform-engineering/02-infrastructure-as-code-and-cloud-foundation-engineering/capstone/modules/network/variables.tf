variable "name" {
  description = "Stable network name."
  type        = string
}

variable "vpc_cidr" {
  description = "IPv4 CIDR owned by this VPC."
  type        = string
}

variable "subnets" {
  description = "Subnets keyed by stable semantic identity."
  type = map(object({
    cidr       = string
    az_id      = string
    tier       = string
    nat_key    = optional(string)
  }))

  validation {
    condition = alltrue([
      for subnet in values(var.subnets) : contains(["public", "private", "data"], subnet.tier)
    ])
    error_message = "subnet tier must be public, private, or data"
  }
}

variable "availability_zone_names_by_id" {
  description = "Map from stable AZ IDs to account-local AZ names."
  type        = map(string)
}

variable "nat_mode" {
  description = "none, single, or per-az."
  type        = string
  default     = "none"

  validation {
    condition     = contains(["none", "single", "per-az"], var.nat_mode)
    error_message = "nat_mode must be none, single, or per-az"
  }
}

variable "enable_s3_endpoint" {
  description = "Create an S3 gateway endpoint for private route tables."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Governed tags from the composition root."
  type        = map(string)
}
