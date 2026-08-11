provider "aws" {
  region = var.aws_region

  # Project Redoubt Phase 11 generates an architecture plan only.
  # These prevent the reference configuration from requiring live
  # AWS identity/account discovery during local security validation.
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_requesting_account_id  = true

  default_tags {
    tags = local.common_tags
  }
}
