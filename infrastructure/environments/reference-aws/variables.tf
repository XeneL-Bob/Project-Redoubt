variable "aws_region" {
  description = "Reference AWS region for the ResTech architecture."
  type        = string
  default     = "ap-southeast-2"
}

variable "environment" {
  description = "Reference deployment environment."
  type        = string
  default     = "reference"
}

variable "project_name" {
  description = "Project identifier."
  type        = string
  default     = "project-redoubt"
}

variable "evidence_bucket_name" {
  description = "Reference security evidence bucket name."
  type        = string
  default     = "restech-redoubt-reference-evidence"
}


variable "security_test_scenario" {
  description = "Phase 11 negative-security test scenario. Must remain none for the compliant reference architecture."
  type        = string
  default     = "none"

  validation {
    condition = contains([
      "none",
      "public-http",
      "public-ssh",
      "management-public-ip",
      "private-default-route",
      "evidence-public-access",
      "evidence-no-kms",
      "evidence-versioning-off",
      "kms-rotation-off",
      "flow-logs-incomplete",
      "missing-security-tags",
      "unrestricted-egress"
    ], var.security_test_scenario)

    error_message = "Unknown Project Redoubt security test scenario."
  }
}
