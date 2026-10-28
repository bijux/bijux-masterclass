variable "name" {
  description = "Stable account-local audit resource prefix."
  type        = string
}

variable "enable_trail" {
  description = "Create the account-local CloudTrail reference implementation."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Governed inventory and cost-allocation tags."
  type        = map(string)
}
