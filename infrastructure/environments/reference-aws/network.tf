resource "aws_vpc" "redoubt" {
  cidr_block           = "10.40.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name               = "redoubt-vpc"
    SecurityZone       = "core"
    DataClassification = "INTERNAL"
  }
}


# ------------------------------------------------------------
# Internet edge
# ------------------------------------------------------------

resource "aws_internet_gateway" "edge" {
  vpc_id = aws_vpc.redoubt.id

  tags = {
    Name         = "redoubt-edge-igw"
    SecurityZone = "edge"
  }
}


# ------------------------------------------------------------
# Security zones
# ------------------------------------------------------------

resource "aws_subnet" "edge" {
  vpc_id                  = aws_vpc.redoubt.id
  cidr_block              = "10.40.10.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = false

  tags = {
    Name               = "redoubt-edge"
    SecurityZone       = "edge"
    DataClassification = "INTERNAL"
  }
}


resource "aws_subnet" "application" {
  vpc_id                  = aws_vpc.redoubt.id
  cidr_block              = "10.40.20.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = false

  tags = {
    Name               = "redoubt-application"
    SecurityZone       = "application"
    DataClassification = "CONFIDENTIAL"
  }
}


resource "aws_subnet" "data" {
  vpc_id                  = aws_vpc.redoubt.id
  cidr_block              = "10.40.30.0/24"
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = false

  tags = {
    Name               = "redoubt-data"
    SecurityZone       = "data"
    DataClassification = "RESTRICTED"
  }
}


resource "aws_subnet" "management" {
  vpc_id            = aws_vpc.redoubt.id
  cidr_block        = "10.40.40.0/24"
  availability_zone = "${var.aws_region}b"

  map_public_ip_on_launch = (
    var.security_test_scenario == "management-public-ip"
  )

  tags = {
    Name               = "redoubt-management"
    SecurityZone       = "management"
    DataClassification = "RESTRICTED"
  }
}


resource "aws_subnet" "recovery" {
  vpc_id                  = aws_vpc.redoubt.id
  cidr_block              = "10.40.50.0/24"
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = false

  tags = {
    Name               = "redoubt-recovery"
    SecurityZone       = "recovery"
    DataClassification = "RESTRICTED"
  }
}


resource "aws_subnet" "telemetry" {
  vpc_id                  = aws_vpc.redoubt.id
  cidr_block              = "10.40.60.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = false

  tags = {
    Name               = "redoubt-telemetry"
    SecurityZone       = "telemetry"
    DataClassification = "RESTRICTED"
  }
}


# ------------------------------------------------------------
# Edge routing
# ------------------------------------------------------------

resource "aws_route_table" "edge" {
  vpc_id = aws_vpc.redoubt.id

  tags = {
    Name         = "redoubt-edge-routes"
    SecurityZone = "edge"
  }
}


resource "aws_route" "edge_internet" {
  route_table_id         = aws_route_table.edge.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.edge.id
}


resource "aws_route_table_association" "edge" {
  subnet_id      = aws_subnet.edge.id
  route_table_id = aws_route_table.edge.id
}


# ------------------------------------------------------------
# Private routing
# ------------------------------------------------------------

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.redoubt.id

  tags = {
    Name         = "redoubt-private-routes"
    SecurityZone = "private"
  }
}


resource "aws_route_table_association" "application" {
  subnet_id      = aws_subnet.application.id
  route_table_id = aws_route_table.private.id
}


resource "aws_route_table_association" "data" {
  subnet_id      = aws_subnet.data.id
  route_table_id = aws_route_table.private.id
}


resource "aws_route_table_association" "management" {
  subnet_id      = aws_subnet.management.id
  route_table_id = aws_route_table.private.id
}


resource "aws_route_table_association" "recovery" {
  subnet_id      = aws_subnet.recovery.id
  route_table_id = aws_route_table.private.id
}


resource "aws_route_table_association" "telemetry" {
  subnet_id      = aws_subnet.telemetry.id
  route_table_id = aws_route_table.private.id
}
