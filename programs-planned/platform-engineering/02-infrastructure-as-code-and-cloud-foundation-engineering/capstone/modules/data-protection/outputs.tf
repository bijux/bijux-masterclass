output "data_volume_id" {
  description = "Separately managed Atlas data volume."
  value       = aws_ebs_volume.atlas.id
}

