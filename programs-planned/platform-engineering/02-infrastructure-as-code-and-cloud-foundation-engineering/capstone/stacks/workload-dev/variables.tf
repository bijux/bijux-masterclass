variable "region" {
  description = "AWS region containing the workload and foundation."
  type        = string
}

variable "environment" {
  description = "Workload environment name."
  type        = string
  default     = "dev"
}

variable "owner" {
  description = "Accountable workload owner."
  type        = string
}

variable "cost_center" {
  description = "Cost-allocation identifier."
  type        = string
}

variable "foundation_contract" {
  description = "Narrow, versioned output contract published by the foundation root."
  type = object({
    vpc_id                    = string
    vpc_cidr                  = string
    public_subnet_ids         = map(string)
    private_subnet_ids        = map(string)
    private_subnet_az_names   = map(string)
    instance_profile_name     = string
    runtime_role_arn          = string
    workload_kms_key_arn      = string
    audit_bucket_arn          = string
    backup_bucket_arn         = string
    governed_tags             = map(string)
  })
}

variable "image_id" {
  description = "Accepted immutable Atlas AMI identifier."
  type        = string
}

variable "architecture" {
  description = "Architecture declared by the accepted image release."
  type        = string
  default     = "amd64"
}

variable "instance_type" {
  description = "Instance type accepted for the declared architecture and resource envelope."
  type        = string
  default     = "t3.micro"
}

variable "certificate_arn" {
  description = "ACM certificate used only when the public edge is enabled."
  type        = string
  default     = null
}

variable "enable_instance" {
  description = "Create the optional cost-bearing sandbox instance."
  type        = bool
  default     = false
}

variable "enable_edge" {
  description = "Create the optional cost-bearing public load balancer."
  type        = bool
  default     = false
}
