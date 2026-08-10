output "vpc_cidr" {
  description = "Project Redoubt reference VPC."
  value       = aws_vpc.redoubt.cidr_block
}


output "security_zones" {
  description = "Reference trust-zone subnet allocation."

  value = {
    edge        = aws_subnet.edge.cidr_block
    application = aws_subnet.application.cidr_block
    data        = aws_subnet.data.cidr_block
    management  = aws_subnet.management.cidr_block
    recovery    = aws_subnet.recovery.cidr_block
    telemetry   = aws_subnet.telemetry.cidr_block
  }
}


output "evidence_controls" {
  description = "Security evidence protection configuration."

  value = {
    bucket             = aws_s3_bucket.evidence.bucket
    kms_key_rotation   = aws_kms_key.evidence.enable_key_rotation
    versioning         = aws_s3_bucket_versioning.evidence.versioning_configuration[0].status
    public_access      = "blocked"
    vpc_flow_log_scope = aws_flow_log.redoubt.traffic_type
  }
}
