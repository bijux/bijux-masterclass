output "prefix" {
  description = "Stable naming prefix for sibling modules."
  value       = local.prefix
}

output "tags" {
  description = "Governed tags for inventory and cost evidence."
  value       = local.tags
}
