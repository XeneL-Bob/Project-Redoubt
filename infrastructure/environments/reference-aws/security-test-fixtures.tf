# ============================================================
# PROJECT REDOUBT — NEGATIVE SECURITY TEST FIXTURES
#
# These resources exist only to generate controlled insecure
# OpenTofu plans for Phase 11 policy validation.
#
# The default security_test_scenario is "none", so none of these
# resources exist in the compliant reference architecture.
# ============================================================


# IAC-001
resource "aws_vpc_security_group_ingress_rule" "test_public_http" {
  count = (
    var.security_test_scenario == "public-http"
    ? 1
    : 0
  )

  security_group_id = aws_security_group.edge.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 80
  to_port     = 80
  ip_protocol = "tcp"

  description = "NEGATIVE TEST — public HTTP"
}


# IAC-001 + IAC-002
resource "aws_vpc_security_group_ingress_rule" "test_public_ssh" {
  count = (
    var.security_test_scenario == "public-ssh"
    ? 1
    : 0
  )

  security_group_id = aws_security_group.management.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 22
  to_port     = 22
  ip_protocol = "tcp"

  description = "NEGATIVE TEST — public SSH"
}


# IAC-004
resource "aws_route" "test_private_internet" {
  count = (
    var.security_test_scenario == "private-default-route"
    ? 1
    : 0
  )

  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.edge.id
}


# IAC-011
resource "aws_vpc_security_group_egress_rule" "test_unrestricted_egress" {
  count = (
    var.security_test_scenario == "unrestricted-egress"
    ? 1
    : 0
  )

  security_group_id = aws_security_group.management.id

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"

  description = "NEGATIVE TEST — unrestricted Internet egress"
}
