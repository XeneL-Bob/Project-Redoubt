resource "aws_kms_key" "evidence" {
  description             = "Project Redoubt security evidence encryption key"
  deletion_window_in_days = 30
  enable_key_rotation = (
    var.security_test_scenario != "kms-rotation-off"
  )

  tags = {
    Name               = "redoubt-evidence"
    SecurityZone       = "security"
    DataClassification = "RESTRICTED"
  }
}


resource "aws_kms_alias" "evidence" {
  name          = "alias/project-redoubt-evidence"
  target_key_id = aws_kms_key.evidence.key_id
}


resource "aws_s3_bucket" "evidence" {
  bucket        = var.evidence_bucket_name
  force_destroy = false

  tags = {
    Name               = "redoubt-security-evidence"
    SecurityZone       = "security"
    DataClassification = "RESTRICTED"
  }
}


resource "aws_s3_bucket_public_access_block" "evidence" {
  bucket = aws_s3_bucket.evidence.id

  block_public_acls = true
  block_public_policy = (
    var.security_test_scenario != "evidence-public-access"
  )
  ignore_public_acls      = true
  restrict_public_buckets = true
}


resource "aws_s3_bucket_versioning" "evidence" {
  bucket = aws_s3_bucket.evidence.id

  versioning_configuration {
    status = (
      var.security_test_scenario == "evidence-versioning-off"
      ? "Suspended"
      : "Enabled"
    )
  }
}


resource "aws_s3_bucket_server_side_encryption_configuration" "evidence" {
  bucket = aws_s3_bucket.evidence.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = (
        var.security_test_scenario == "evidence-no-kms"
        ? null
        : aws_kms_key.evidence.arn
      )

      sse_algorithm = (
        var.security_test_scenario == "evidence-no-kms"
        ? "AES256"
        : "aws:kms"
      )
    }

    bucket_key_enabled = true
  }
}


resource "aws_flow_log" "redoubt" {
  vpc_id = aws_vpc.redoubt.id

  traffic_type = (
    var.security_test_scenario == "flow-logs-incomplete"
    ? "ACCEPT"
    : "ALL"
  )

  log_destination      = aws_s3_bucket.evidence.arn
  log_destination_type = "s3"

  destination_options {
    file_format        = "parquet"
    per_hour_partition = true
  }

  tags = {
    Name               = "redoubt-vpc-flow-logs"
    SecurityZone       = "telemetry"
    DataClassification = "RESTRICTED"
  }
}
