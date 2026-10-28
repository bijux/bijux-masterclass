run "valid_prefix_and_tags" {
  command = plan

  variables {
    system       = "atlas"
    environment  = "dev"
    region_code  = "euc1"
    owner        = "platform-team"
    cost_center  = "education"
  }

  assert {
    condition     = output.prefix == "atlas-dev-euc1"
    error_message = "prefix must be stable and lower-case"
  }

  assert {
    condition     = output.tags["atlas:managed-by"] == "opentofu"
    error_message = "managed-by tag is required"
  }
}
