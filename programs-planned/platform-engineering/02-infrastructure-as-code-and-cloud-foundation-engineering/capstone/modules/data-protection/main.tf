resource "aws_ebs_volume" "atlas" {
  availability_zone = var.availability_zone
  size              = var.volume_size_gib
  type              = "gp3"
  encrypted         = true
  kms_key_id        = var.kms_key_arn
  tags              = merge(var.tags, { Name = "${var.name}-data" })
}
