variable "name" {
  description = "Stable Atlas workload name."
  type        = string
}

variable "image_id" {
  description = "Immutable AMI identifier accepted by the image release process."
  type        = string

  validation {
    condition     = can(regex("^ami-[0-9a-f]+$", var.image_id))
    error_message = "image_id must be an AMI identifier, not a mutable name such as latest."
  }
}

variable "architecture" {
  description = "Architecture declared by the accepted image release."
  type        = string

  validation {
    condition     = contains(["amd64", "arm64"], var.architecture)
    error_message = "architecture must be amd64 or arm64."
  }
}

variable "instance_type" {
  description = "EC2 instance type reviewed against the image architecture and resource envelope."
  type        = string
}

variable "subnet_id" {
  description = "Private subnet selected by the composition root."
  type        = string
}

variable "security_group_ids" {
  description = "Security groups attached to the primary workload interface."
  type        = list(string)
}

variable "instance_profile_name" {
  description = "Foundation-owned runtime instance profile."
  type        = string
}

variable "data_volume_id" {
  description = "Separately managed durable Atlas data volume."
  type        = string
}

variable "data_device_name" {
  description = "Requested Linux device name for the durable data volume."
  type        = string
  default     = "/dev/sdf"
}

variable "enable_instance" {
  description = "Create the optional sandbox instance."
  type        = bool
  default     = false
}

variable "bootstrap_profile_version" {
  description = "Versioned host-runtime contract already installed in the image."
  type        = string
}

variable "tags" {
  description = "Governed inventory and cost-allocation tags."
  type        = map(string)
}
