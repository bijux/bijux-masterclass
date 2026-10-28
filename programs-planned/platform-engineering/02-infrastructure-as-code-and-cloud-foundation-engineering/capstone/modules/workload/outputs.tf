output "launch_template_id" {
  description = "Versioned launch definition for Atlas replacement."
  value       = aws_launch_template.atlas.id
}

output "launch_template_latest_version" {
  description = "Latest launch-template version; releases record an explicit selected version."
  value       = aws_launch_template.atlas.latest_version
}

output "instance_id" {
  description = "Optional sandbox instance identity."
  value       = try(aws_instance.atlas[0].id, null)
}
