data "aws_iam_policy_document" "ec2_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_kms_key" "workload" {
  description             = "Atlas ${var.environment} workload data"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  tags                    = var.tags
}

resource "aws_kms_alias" "workload" {
  name          = "alias/${var.name}-data"
  target_key_id = aws_kms_key.workload.key_id
}

resource "aws_iam_role" "runtime" {
  name               = "${var.name}-runtime"
  assume_role_policy = data.aws_iam_policy_document.ec2_trust.json
  tags               = var.tags
}

data "aws_iam_policy_document" "runtime" {
  statement {
    sid       = "ReadAtlasConfiguration"
    effect    = "Allow"
    actions   = ["ssm:GetParameter", "ssm:GetParameters"]
    resources = ["arn:aws:ssm:${var.region}:${var.account_id}:parameter/${var.config_parameter_prefix}*"]
  }

  statement {
    sid       = "ReadAtlasSecrets"
    effect    = "Allow"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = ["arn:aws:secretsmanager:${var.region}:${var.account_id}:secret:${var.secret_prefix}*"]
  }

  statement {
    sid       = "UseWorkloadKey"
    effect    = "Allow"
    actions   = ["kms:Decrypt", "kms:Encrypt", "kms:GenerateDataKey"]
    resources = [aws_kms_key.workload.arn]
  }

  statement {
    sid       = "WriteAtlasBackup"
    effect    = "Allow"
    actions   = ["s3:PutObject", "s3:AbortMultipartUpload"]
    resources = ["${var.backup_bucket_arn}/results/*"]
  }
}

resource "aws_iam_role_policy" "runtime" {
  name   = "${var.name}-runtime"
  role   = aws_iam_role.runtime.id
  policy = data.aws_iam_policy_document.runtime.json
}

resource "aws_iam_instance_profile" "runtime" {
  name = "${var.name}-runtime"
  role = aws_iam_role.runtime.name
  tags = var.tags
}
