variable "system" {
  description = "Stable system identifier."
  type        = string
}

variable "environment" {
  description = "Environment identifier such as dev or prod."
  type        = string
}

variable "region_code" {
  description = "Short governed region code, for example euc1."
  type        = string
}

variable "owner" {
  description = "Accountable owner used in tags."
  type        = string
}

variable "cost_center" {
  description = "Cost allocation identifier."
  type        = string
}

variable "extra_tags" {
  description = "Additional non-authoritative inventory tags."
  type        = map(string)
  default     = {}
}
