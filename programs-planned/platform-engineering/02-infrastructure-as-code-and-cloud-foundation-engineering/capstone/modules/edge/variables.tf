variable "name" {
  description = "Stable Atlas edge name."
  type        = string
}

variable "vpc_id" {
  description = "VPC that owns the load balancer and target group."
  type        = string
}

variable "public_subnet_ids" {
  description = "Public subnets in at least two distinct availability zones."
  type        = list(string)
}

variable "host_security_group_id" {
  description = "Security group attached to the private Atlas host."
  type        = string
}

variable "target_instance_id" {
  description = "Optional sandbox instance registered with the target group."
  type        = string
  default     = null
}

variable "enable_target_attachment" {
  description = "Register the optional sandbox instance as a target."
  type        = bool
  default     = false
}

variable "certificate_arn" {
  description = "ACM certificate ARN for the HTTPS listener."
  type        = string
  default     = null
}

variable "enable_edge" {
  description = "Create the cost-bearing public load-balancer edge."
  type        = bool
  default     = false
}

variable "tags" {
  description = "Governed inventory and cost-allocation tags."
  type        = map(string)
}
