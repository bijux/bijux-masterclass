moved {
  from = aws_vpc.atlas
  to   = module.network.aws_vpc.this
}

moved {
  from = aws_subnet.private_a
  to   = module.network.aws_subnet.this["private-a"]
}
