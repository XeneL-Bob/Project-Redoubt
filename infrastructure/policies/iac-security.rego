package redoubt.iac.security

import rego.v1


security_sensitive_types := {
    "aws_vpc",
    "aws_subnet",
    "aws_security_group",
    "aws_kms_key",
    "aws_s3_bucket",
    "aws_flow_log",
}


internet_source(after) if {
    object.get(after, "cidr_ipv4", "") == "0.0.0.0/0"
}

internet_source(after) if {
    object.get(after, "cidr_ipv6", "") == "::/0"
}


https_only(after) if {
    object.get(after, "ip_protocol", "") == "tcp"
    object.get(after, "from_port", -1) == 443
    object.get(after, "to_port", -1) == 443
}


port_exposed(after, port) if {
    object.get(after, "ip_protocol", "") == "tcp"

    from_port := object.get(
        after,
        "from_port",
        -1,
    )

    to_port := object.get(
        after,
        "to_port",
        -1,
    )

    from_port <= port
    to_port >= port
}


required_tags_present(after) if {
    tags := object.get(
        after,
        "tags",
        {},
    )

    object.get(
        tags,
        "SecurityZone",
        "",
    ) != ""

    object.get(
        tags,
        "DataClassification",
        "",
    ) != ""
}


public_access_block_complete(after) if {
    object.get(
        after,
        "block_public_acls",
        false,
    ) == true

    object.get(
        after,
        "block_public_policy",
        false,
    ) == true

    object.get(
        after,
        "ignore_public_acls",
        false,
    ) == true

    object.get(
        after,
        "restrict_public_buckets",
        false,
    ) == true
}


kms_encryption_enabled(after) if {
    some rule in object.get(
        after,
        "rule",
        [],
    )

    some encryption in object.get(
        rule,
        "apply_server_side_encryption_by_default",
        [],
    )

    object.get(
        encryption,
        "sse_algorithm",
        "",
    ) == "aws:kms"
}


versioning_enabled(after) if {
    some config in object.get(
        after,
        "versioning_configuration",
        [],
    )

    object.get(
        config,
        "status",
        "",
    ) == "Enabled"
}


# ------------------------------------------------------------
# IAC-001
# Internet-exposed ingress must be HTTPS only.
# ------------------------------------------------------------

deny contains violation if {
    rc := input.resource_changes[_]

    rc.type ==
        "aws_vpc_security_group_ingress_rule"

    after := object.get(
        rc.change,
        "after",
        {},
    )

    internet_source(after)
    not https_only(after)

    violation := {
        "id": "IAC-001",
        "resource": rc.address,
        "message":
            "Internet-exposed ingress must be TCP/443 only",
    }
}


# ------------------------------------------------------------
# IAC-002
# SSH must never be Internet exposed.
# ------------------------------------------------------------

deny contains violation if {
    rc := input.resource_changes[_]

    rc.type ==
        "aws_vpc_security_group_ingress_rule"

    after := object.get(
        rc.change,
        "after",
        {},
    )

    internet_source(after)
    port_exposed(after, 22)

    violation := {
        "id": "IAC-002",
        "resource": rc.address,
        "message":
            "SSH must not be exposed to the Internet",
    }
}


# ------------------------------------------------------------
# IAC-003
# Non-edge subnets cannot assign public addresses.
# ------------------------------------------------------------

deny contains violation if {
    rc := input.resource_changes[_]
    rc.type == "aws_subnet"

    after := object.get(
        rc.change,
        "after",
        {},
    )

    tags := object.get(
        after,
        "tags",
        {},
    )

    zone := object.get(
        tags,
        "SecurityZone",
        "",
    )

    zone != ""
    zone != "edge"

    object.get(
        after,
        "map_public_ip_on_launch",
        false,
    ) == true

    violation := {
        "id": "IAC-003",
        "resource": rc.address,
        "message":
            sprintf(
                "%s subnet may not automatically assign public IP addresses",
                [zone],
            ),
    }
}


# ------------------------------------------------------------
# IAC-004
# Only the defined edge route may have a default Internet route.
# ------------------------------------------------------------

deny contains violation if {
    rc := input.resource_changes[_]
    rc.type == "aws_route"

    after := object.get(
        rc.change,
        "after",
        {},
    )

    object.get(
        after,
        "destination_cidr_block",
        "",
    ) == "0.0.0.0/0"

    rc.address !=
        "aws_route.edge_internet"

    violation := {
        "id": "IAC-004",
        "resource": rc.address,
        "message":
            "Default Internet routes are permitted only in the edge trust zone",
    }
}


# ------------------------------------------------------------
# IAC-005
# Evidence storage public-access protection is mandatory.
# ------------------------------------------------------------

deny contains violation if {
    rc := input.resource_changes[_]

    rc.type ==
        "aws_s3_bucket_public_access_block"

    after := object.get(
        rc.change,
        "after",
        {},
    )

    not public_access_block_complete(after)

    violation := {
        "id": "IAC-005",
        "resource": rc.address,
        "message":
            "Security evidence storage must block all forms of public access",
    }
}


# ------------------------------------------------------------
# IAC-006
# S3 evidence encryption must use AWS KMS.
# ------------------------------------------------------------

deny contains violation if {
    rc := input.resource_changes[_]

    rc.type ==
        "aws_s3_bucket_server_side_encryption_configuration"

    after := object.get(
        rc.change,
        "after",
        {},
    )

    not kms_encryption_enabled(after)

    violation := {
        "id": "IAC-006",
        "resource": rc.address,
        "message":
            "Security evidence storage must use AWS KMS encryption",
    }
}


# ------------------------------------------------------------
# IAC-007
# Evidence versioning must remain enabled.
# ------------------------------------------------------------

deny contains violation if {
    rc := input.resource_changes[_]

    rc.type ==
        "aws_s3_bucket_versioning"

    after := object.get(
        rc.change,
        "after",
        {},
    )

    not versioning_enabled(after)

    violation := {
        "id": "IAC-007",
        "resource": rc.address,
        "message":
            "Security evidence storage versioning must remain enabled",
    }
}


# ------------------------------------------------------------
# IAC-008
# KMS key rotation is mandatory.
# ------------------------------------------------------------

deny contains violation if {
    rc := input.resource_changes[_]
    rc.type == "aws_kms_key"

    after := object.get(
        rc.change,
        "after",
        {},
    )

    object.get(
        after,
        "enable_key_rotation",
        false,
    ) != true

    violation := {
        "id": "IAC-008",
        "resource": rc.address,
        "message":
            "KMS key rotation must be enabled",
    }
}


# ------------------------------------------------------------
# IAC-009
# Network telemetry must capture all traffic.
# ------------------------------------------------------------

deny contains violation if {
    rc := input.resource_changes[_]
    rc.type == "aws_flow_log"

    after := object.get(
        rc.change,
        "after",
        {},
    )

    object.get(
        after,
        "traffic_type",
        "",
    ) != "ALL"

    violation := {
        "id": "IAC-009",
        "resource": rc.address,
        "message":
            "VPC flow logging must capture ALL traffic",
    }
}


# ------------------------------------------------------------
# IAC-010
# Security-sensitive resources require architectural metadata.
# ------------------------------------------------------------

deny contains violation if {
    rc := input.resource_changes[_]

    rc.type in security_sensitive_types

    after := object.get(
        rc.change,
        "after",
        {},
    )

    not required_tags_present(after)

    violation := {
        "id": "IAC-010",
        "resource": rc.address,
        "message":
            "Security-sensitive infrastructure requires SecurityZone and DataClassification tags",
    }
}


# ------------------------------------------------------------
# IAC-011
# Security groups may not permit unrestricted Internet egress.
# ------------------------------------------------------------

deny contains violation if {
    rc := input.resource_changes[_]

    rc.type ==
        "aws_vpc_security_group_egress_rule"

    after := object.get(
        rc.change,
        "after",
        {},
    )

    internet_source(after)

    violation := {
        "id": "IAC-011",
        "resource": rc.address,
        "message":
            "Unrestricted security-group Internet egress is prohibited",
    }
}
