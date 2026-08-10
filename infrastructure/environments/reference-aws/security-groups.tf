resource "aws_security_group" "edge" {
  name        = "redoubt-edge"
  description = "Public Policy Enforcement Point"
  vpc_id      = aws_vpc.redoubt.id

  tags = {
    SecurityZone       = "edge"
    DataClassification = "INTERNAL"
  }
}


resource "aws_security_group" "application" {
  name        = "redoubt-application"
  description = "Protected application workloads"
  vpc_id      = aws_vpc.redoubt.id

  tags = {
    SecurityZone       = "application"
    DataClassification = "CONFIDENTIAL"
  }
}


resource "aws_security_group" "data" {
  name        = "redoubt-data"
  description = "Restricted data tier"
  vpc_id      = aws_vpc.redoubt.id

  tags = {
    SecurityZone       = "data"
    DataClassification = "RESTRICTED"
  }
}


resource "aws_security_group" "management" {
  name        = "redoubt-management"
  description = "Privileged management plane"
  vpc_id      = aws_vpc.redoubt.id

  tags = {
    SecurityZone = "management"

    DataClassification = (
      var.security_test_scenario == "missing-security-tags"
      ? ""
      : "RESTRICTED"
    )
  }
}


resource "aws_security_group" "recovery" {
  name        = "redoubt-recovery"
  description = "Isolated recovery plane"
  vpc_id      = aws_vpc.redoubt.id

  tags = {
    SecurityZone       = "recovery"
    DataClassification = "RESTRICTED"
  }
}


resource "aws_security_group" "telemetry" {
  name        = "redoubt-telemetry"
  description = "Central security telemetry plane"
  vpc_id      = aws_vpc.redoubt.id

  tags = {
    SecurityZone       = "telemetry"
    DataClassification = "RESTRICTED"
  }
}


# ------------------------------------------------------------
# Internet -> Edge
# ------------------------------------------------------------

resource "aws_vpc_security_group_ingress_rule" "edge_https" {
  security_group_id = aws_security_group.edge.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"

  description = "Public HTTPS ingress to the policy enforcement edge"
}


# ------------------------------------------------------------
# Edge -> Application
# ------------------------------------------------------------

resource "aws_vpc_security_group_egress_rule" "edge_application" {
  security_group_id = aws_security_group.edge.id

  referenced_security_group_id = aws_security_group.application.id

  from_port   = 8443
  to_port     = 8443
  ip_protocol = "tcp"

  description = "Edge may invoke protected application workloads"
}


resource "aws_vpc_security_group_ingress_rule" "application_edge" {
  security_group_id = aws_security_group.application.id

  referenced_security_group_id = aws_security_group.edge.id

  from_port   = 8443
  to_port     = 8443
  ip_protocol = "tcp"

  description = "Applications accept only the trusted edge path"
}


# ------------------------------------------------------------
# Application -> Data
# ------------------------------------------------------------

resource "aws_vpc_security_group_egress_rule" "application_data" {
  security_group_id = aws_security_group.application.id

  referenced_security_group_id = aws_security_group.data.id

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"

  description = "Application access to the restricted data tier"
}


resource "aws_vpc_security_group_ingress_rule" "data_application" {
  security_group_id = aws_security_group.data.id

  referenced_security_group_id = aws_security_group.application.id

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"

  description = "Database access only from approved application workloads"
}


# ------------------------------------------------------------
# Workloads -> Telemetry
# ------------------------------------------------------------

resource "aws_vpc_security_group_egress_rule" "application_telemetry" {
  security_group_id = aws_security_group.application.id

  referenced_security_group_id = aws_security_group.telemetry.id

  from_port   = 9000
  to_port     = 9000
  ip_protocol = "tcp"

  description = "Application security telemetry"
}


resource "aws_vpc_security_group_egress_rule" "management_telemetry" {
  security_group_id = aws_security_group.management.id

  referenced_security_group_id = aws_security_group.telemetry.id

  from_port   = 9000
  to_port     = 9000
  ip_protocol = "tcp"

  description = "Management-plane security telemetry"
}


resource "aws_vpc_security_group_ingress_rule" "telemetry_application" {
  security_group_id = aws_security_group.telemetry.id

  referenced_security_group_id = aws_security_group.application.id

  from_port   = 9000
  to_port     = 9000
  ip_protocol = "tcp"

  description = "Telemetry ingestion from application workloads"
}


resource "aws_vpc_security_group_ingress_rule" "telemetry_management" {
  security_group_id = aws_security_group.telemetry.id

  referenced_security_group_id = aws_security_group.management.id

  from_port   = 9000
  to_port     = 9000
  ip_protocol = "tcp"

  description = "Telemetry ingestion from management workloads"
}
