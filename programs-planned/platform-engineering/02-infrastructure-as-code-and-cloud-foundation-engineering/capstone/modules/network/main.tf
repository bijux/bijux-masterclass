locals {
  public_subnets  = { for key, value in var.subnets : key => value if value.tier == "public" }
  private_subnets = { for key, value in var.subnets : key => value if value.tier == "private" }
  data_subnets    = { for key, value in var.subnets : key => value if value.tier == "data" }

  nat_keys = var.nat_mode == "single" && length(local.public_subnets) > 0 ? (
    toset([sort(keys(local.public_subnets))[0]])
  ) : var.nat_mode == "per-az" ? (
    toset(keys(local.public_subnets))
  ) : toset([])
}

resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = merge(var.tags, { Name = var.name })
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
  tags   = merge(var.tags, { Name = "${var.name}-igw" })
}

resource "aws_subnet" "this" {
  for_each = var.subnets

  vpc_id                  = aws_vpc.this.id
  cidr_block              = each.value.cidr
  availability_zone       = var.availability_zone_names_by_id[each.value.az_id]
  map_public_ip_on_launch = false
  tags = merge(var.tags, {
    Name         = "${var.name}-${each.key}"
    "atlas:tier" = each.value.tier
    "atlas:az-id" = each.value.az_id
  })
}

resource "aws_route_table" "public" {
  for_each = local.public_subnets
  vpc_id   = aws_vpc.this.id
  tags     = merge(var.tags, { Name = "${var.name}-${each.key}-public" })
}

resource "aws_route" "public_default" {
  for_each               = local.public_subnets
  route_table_id         = aws_route_table.public[each.key].id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.this.id
}

resource "aws_route_table_association" "public" {
  for_each       = local.public_subnets
  subnet_id      = aws_subnet.this[each.key].id
  route_table_id = aws_route_table.public[each.key].id
}

resource "aws_eip" "nat" {
  for_each = local.nat_keys
  domain   = "vpc"
  tags     = merge(var.tags, { Name = "${var.name}-${each.key}-nat-eip" })

  depends_on = [aws_internet_gateway.this]
}

resource "aws_nat_gateway" "this" {
  for_each      = local.nat_keys
  allocation_id = aws_eip.nat[each.key].id
  subnet_id     = aws_subnet.this[each.key].id
  tags          = merge(var.tags, { Name = "${var.name}-${each.key}-nat" })
}

resource "aws_route_table" "private" {
  for_each = local.private_subnets
  vpc_id   = aws_vpc.this.id
  tags     = merge(var.tags, { Name = "${var.name}-${each.key}-private" })
}

locals {
  first_nat_key = length(local.nat_keys) > 0 ? sort(tolist(local.nat_keys))[0] : null
  private_nat_key = {
    for key, subnet in local.private_subnets : key => (
      var.nat_mode == "per-az" ? (
        subnet.nat_key != null ? subnet.nat_key : local.first_nat_key
      ) : local.first_nat_key
    )
  }
}

resource "aws_route" "private_default" {
  for_each = var.nat_mode == "none" ? {} : local.private_subnets

  route_table_id         = aws_route_table.private[each.key].id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = try(aws_nat_gateway.this[local.private_nat_key[each.key]].id, null)
}

resource "aws_route_table_association" "private" {
  for_each       = local.private_subnets
  subnet_id      = aws_subnet.this[each.key].id
  route_table_id = aws_route_table.private[each.key].id
}

resource "aws_route_table" "data" {
  for_each = local.data_subnets
  vpc_id   = aws_vpc.this.id
  tags     = merge(var.tags, { Name = "${var.name}-${each.key}-data" })
}

resource "aws_route_table_association" "data" {
  for_each       = local.data_subnets
  subnet_id      = aws_subnet.this[each.key].id
  route_table_id = aws_route_table.data[each.key].id
}

resource "aws_vpc_endpoint" "s3" {
  count             = var.enable_s3_endpoint ? 1 : 0
  vpc_id            = aws_vpc.this.id
  service_name      = "com.amazonaws.${data.aws_region.current.name}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids = concat(
    [for table in aws_route_table.private : table.id],
    [for table in aws_route_table.data : table.id],
  )
  tags = merge(var.tags, { Name = "${var.name}-s3" })
}

data "aws_region" "current" {}

check "known_availability_zone_ids" {
  assert {
    condition = alltrue([
      for subnet in values(var.subnets) : contains(keys(var.availability_zone_names_by_id), subnet.az_id)
    ])
    error_message = "Every subnet az_id must exist in availability_zone_names_by_id."
  }
}

check "nat_topology" {
  assert {
    condition = var.nat_mode == "none" || (
      length(local.public_subnets) > 0 &&
      (
        var.nat_mode != "per-az" || alltrue([
          for subnet in values(local.private_subnets) :
          subnet.nat_key != null && try(contains(keys(local.public_subnets), subnet.nat_key), false)
        ])
      )
    )
    error_message = "NAT requires a public subnet; per-az mode requires each private subnet to name an existing public nat_key."
  }
}
