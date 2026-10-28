locals {
  user_data = <<-EOT
    #!/bin/sh
    set -eu
    install -d -m 0755 /etc/atlas
    printf '%s\n' '${var.bootstrap_profile_version}' > /etc/atlas/bootstrap-profile
    systemctl daemon-reload
    systemctl enable atlas-api atlas-worker
    systemctl start atlas-api atlas-worker
  EOT
}

resource "aws_launch_template" "atlas" {
  name_prefix   = "${var.name}-"
  image_id      = var.image_id
  instance_type = var.instance_type
  user_data     = base64encode(local.user_data)

  iam_instance_profile {
    name = var.instance_profile_name
  }

  vpc_security_group_ids = var.security_group_ids

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
    instance_metadata_tags      = "disabled"
  }

  tag_specifications {
    resource_type = "instance"
    tags = merge(var.tags, {
      Name                 = var.name
      "atlas:architecture" = var.architecture
      "atlas:image-id"     = var.image_id
    })
  }

  tag_specifications {
    resource_type = "volume"
    tags          = var.tags
  }

  update_default_version = false
}

resource "aws_instance" "atlas" {
  count = var.enable_instance ? 1 : 0

  subnet_id = var.subnet_id

  launch_template {
    id      = aws_launch_template.atlas.id
    version = aws_launch_template.atlas.latest_version
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_volume_attachment" "data" {
  count = var.enable_instance ? 1 : 0

  device_name = var.data_device_name
  volume_id   = var.data_volume_id
  instance_id = aws_instance.atlas[0].id
}
