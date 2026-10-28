provider "aws" {
  region = var.region
}

data "aws_caller_identity" "target" {}

check "target_account" {
  assert {
    condition     = data.aws_caller_identity.target.account_id == var.account_id
    error_message = "AWS caller account does not match the declared target account."
  }
}

module "naming" {
  source = "../../modules/naming"

  system      = "atlas"
  environment = var.environment
  region_code = "euc1"
  owner       = var.owner
  cost_center = var.cost_center
}

module "network" {
  source = "../../modules/network"

  name                          = module.naming.prefix
  vpc_cidr                      = var.vpc_cidr
  availability_zone_names_by_id = var.availability_zone_names_by_id
  nat_mode                      = var.nat_mode
  tags                          = module.naming.tags
  subnets = {
    public-a  = { cidr = "10.64.0.0/24",  az_id = "euc1-az1", tier = "public" }
    public-b  = { cidr = "10.64.1.0/24",  az_id = "euc1-az2", tier = "public" }
    private-a = { cidr = "10.64.16.0/20", az_id = "euc1-az1", tier = "private", nat_key = "public-a" }
    private-b = { cidr = "10.64.32.0/20", az_id = "euc1-az2", tier = "private", nat_key = "public-b" }
    data-a    = { cidr = "10.64.64.0/24", az_id = "euc1-az1", tier = "data" }
    data-b    = { cidr = "10.64.65.0/24", az_id = "euc1-az2", tier = "data" }
  }
}

# The backup bucket is composed before the identity module so the runtime policy
# can be scoped to the exact bucket ARN.
resource "aws_s3_bucket" "backup" {
  bucket = var.backup_bucket_name
  tags   = module.naming.tags
}

resource "aws_s3_bucket_versioning" "backup" {
  bucket = aws_s3_bucket.backup.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "backup" {
  bucket                  = aws_s3_bucket.backup.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_iam_policy_document" "backup" {
  statement {
    sid    = "DenyInsecureTransport"
    effect = "Deny"
    actions = ["s3:*"]
    resources = [aws_s3_bucket.backup.arn, "${aws_s3_bucket.backup.arn}/*"]

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "backup" {
  bucket = aws_s3_bucket.backup.id
  policy = data.aws_iam_policy_document.backup.json
}

module "identity" {
  source = "../../modules/identity"

  name                    = module.naming.prefix
  region                  = var.region
  account_id              = var.account_id
  environment             = var.environment
  config_parameter_prefix = "atlas/${var.environment}/config/"
  secret_prefix           = "atlas/${var.environment}/"
  backup_bucket_arn       = aws_s3_bucket.backup.arn
  tags                     = module.naming.tags
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backup" {
  bucket = aws_s3_bucket.backup.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = module.identity.workload_kms_key_arn
      sse_algorithm     = "aws:kms"
    }

    bucket_key_enabled = true
  }
}

module "audit" {
  source = "../../modules/audit"

  name         = module.naming.prefix
  enable_trail = var.audit_enabled
  tags         = module.naming.tags
}
