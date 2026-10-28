locals {
  prefix = lower(join("-", [var.system, var.environment, var.region_code]))

  tags = merge({
    "atlas:owner"       = var.owner
    "atlas:environment" = var.environment
    "atlas:system"      = var.system
    "atlas:managed-by"  = "opentofu"
    "atlas:cost-center" = var.cost_center
  }, var.extra_tags)
}
