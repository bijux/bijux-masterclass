terraform {
  required_version = ">= 1.12.5, < 1.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.58.0"
    }
  }
}
