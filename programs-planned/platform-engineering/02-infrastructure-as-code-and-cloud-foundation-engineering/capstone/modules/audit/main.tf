data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_region" "current" {}

locals {
  trail_name = "${var.name}-account-trail"
  trail_arn  = "arn:${data.aws_partition.current.partition}:cloudtrail:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:trail/${local.trail_name}"
}

data "aws_iam_policy_document" "audit_key" {
  statement {
    sid    = "EnableAccountAdministration"
    effect = "Allow"
    actions = ["kms:*"]
    resources = ["*"]

    principals {
      type        = "AWS"
      identifiers = ["arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
  }

  statement {
    sid    = "AllowCloudTrailEncryption"
    effect = "Allow"
    actions = ["kms:GenerateDataKey*"]
    resources = ["*"]

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [local.trail_arn]
    }

    condition {
      test     = "StringLike"
      variable = "kms:EncryptionContext:aws:cloudtrail:arn"
      values   = ["arn:${data.aws_partition.current.partition}:cloudtrail:*:${data.aws_caller_identity.current.account_id}:trail/*"]
    }
  }

  statement {
    sid    = "AllowCloudTrailDescribeKey"
    effect = "Allow"
    actions = ["kms:DescribeKey"]
    resources = ["*"]

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
  }
}

resource "aws_kms_key" "audit" {
  description             = "Account-local Atlas audit evidence"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  policy                  = data.aws_iam_policy_document.audit_key.json
  tags                    = var.tags
}

resource "aws_s3_bucket" "audit" {
  bucket_prefix = "${var.name}-audit-"
  tags          = var.tags
}

resource "aws_s3_bucket_versioning" "audit" {
  bucket = aws_s3_bucket.audit.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "audit" {
  bucket = aws_s3_bucket.audit.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.audit.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "audit" {
  bucket                  = aws_s3_bucket.audit.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_iam_policy_document" "audit_bucket" {
  statement {
    sid    = "AWSCloudTrailAclCheck"
    effect = "Allow"
    actions = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.audit.arn]

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [local.trail_arn]
    }
  }

  statement {
    sid    = "AWSCloudTrailWrite"
    effect = "Allow"
    actions = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.audit.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*"]

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [local.trail_arn]
    }
  }

  statement {
    sid    = "DenyInsecureTransport"
    effect = "Deny"
    actions = ["s3:*"]
    resources = [aws_s3_bucket.audit.arn, "${aws_s3_bucket.audit.arn}/*"]

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

resource "aws_s3_bucket_policy" "audit" {
  bucket = aws_s3_bucket.audit.id
  policy = data.aws_iam_policy_document.audit_bucket.json
}

# This is an account-local trail for the executable sandbox lane. It is not
# equivalent to an organization trail delivered into an independent log archive.
resource "aws_cloudtrail" "account" {
  count = var.enable_trail ? 1 : 0

  name                          = local.trail_name
  s3_bucket_name                = aws_s3_bucket.audit.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true
  kms_key_id                    = aws_kms_key.audit.arn
  tags                          = var.tags

  depends_on = [aws_s3_bucket_policy.audit]
}
