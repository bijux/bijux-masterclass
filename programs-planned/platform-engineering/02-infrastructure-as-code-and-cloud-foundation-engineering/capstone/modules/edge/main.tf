resource "aws_security_group" "edge" {
  count = var.enable_edge ? 1 : 0

  name_prefix = "${var.name}-edge-"
  description = "Public TLS edge for Atlas"
  vpc_id      = var.vpc_id
  tags        = var.tags

  ingress {
    description = "HTTPS from the internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    description     = "Atlas target only"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [var.host_security_group_id]
  }
}

resource "aws_lb" "atlas" {
  count = var.enable_edge ? 1 : 0

  name               = substr(var.name, 0, 32)
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.edge[0].id]
  subnets            = var.public_subnet_ids
  tags               = var.tags
}

resource "aws_lb_target_group" "atlas" {
  count = var.enable_edge ? 1 : 0

  name        = substr("${var.name}-api", 0, 32)
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "instance"

  deregistration_delay = 30

  health_check {
    enabled             = true
    path                = "/edge-health"
    protocol            = "HTTP"
    interval            = 15
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
    matcher             = "200"
  }

  tags = var.tags
}

resource "aws_lb_target_group_attachment" "atlas" {
  count = var.enable_edge && var.enable_target_attachment ? 1 : 0

  target_group_arn = aws_lb_target_group.atlas[0].arn
  target_id        = var.target_instance_id
  port             = 8080
}

resource "aws_lb_listener" "https" {
  count = var.enable_edge && var.certificate_arn != null ? 1 : 0

  load_balancer_arn = aws_lb.atlas[0].arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.atlas[0].arn
  }
}

check "edge_inputs" {
  assert {
    condition = !var.enable_edge || (
      var.certificate_arn != null &&
      length(distinct(var.public_subnet_ids)) >= 2
    )
    error_message = "The public edge requires a certificate and at least two distinct public subnet IDs."
  }
}

check "target_attachment_inputs" {
  assert {
    condition     = !var.enable_target_attachment || (var.enable_edge && var.target_instance_id != null)
    error_message = "Target attachment requires an enabled edge and a non-null target instance ID."
  }
}
