provider "aws" {
  region = var.region
}

module "naming" {
  source = "../../modules/naming"

  system      = "atlas"
  environment = var.environment
  region_code = "euc1"
  owner       = var.owner
  cost_center = var.cost_center
}

resource "aws_security_group" "host" {
  name_prefix = "${module.naming.prefix}-host-"
  description = "Private Atlas host; ingress is added only from the edge"
  vpc_id      = var.foundation_contract.vpc_id
  tags        = module.naming.tags

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "data_protection" {
  source = "../../modules/data-protection"

  name               = module.naming.prefix
  availability_zone  = var.foundation_contract.private_subnet_az_names["private-a"]
  kms_key_arn        = var.foundation_contract.workload_kms_key_arn
  tags               = module.naming.tags
}

module "workload" {
  source = "../../modules/workload"

  name                     = module.naming.prefix
  image_id                 = var.image_id
  architecture             = var.architecture
  instance_type            = var.instance_type
  subnet_id                = var.foundation_contract.private_subnet_ids["private-a"]
  security_group_ids       = [aws_security_group.host.id]
  instance_profile_name    = var.foundation_contract.instance_profile_name
  data_volume_id           = module.data_protection.data_volume_id
  enable_instance          = var.enable_instance
  bootstrap_profile_version = "atlas-host-runtime-1.0"
  tags                      = module.naming.tags
}

module "edge" {
  source = "../../modules/edge"

  name                   = module.naming.prefix
  vpc_id                 = var.foundation_contract.vpc_id
  public_subnet_ids       = values(var.foundation_contract.public_subnet_ids)
  host_security_group_id  = aws_security_group.host.id
  target_instance_id       = module.workload.instance_id
  enable_target_attachment = var.enable_instance
  certificate_arn          = var.certificate_arn
  enable_edge             = var.enable_edge
  tags                    = module.naming.tags
}

resource "aws_security_group_rule" "edge_to_host" {
  count = var.enable_edge ? 1 : 0

  type                     = "ingress"
  description              = "Atlas API from governed edge only"
  from_port                = 8080
  to_port                  = 8080
  protocol                 = "tcp"
  security_group_id        = aws_security_group.host.id
  source_security_group_id = module.edge.edge_security_group_id
}
