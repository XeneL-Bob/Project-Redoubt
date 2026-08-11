locals {
  common_tags = {
    Project      = var.project_name
    Organisation = "ResTech"
    Environment  = var.environment
    ManagedBy    = "OpenTofu"
    Security     = "Project-Redoubt"
  }
}
