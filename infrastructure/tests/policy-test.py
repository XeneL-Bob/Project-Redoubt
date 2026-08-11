#!/usr/bin/env python3

import copy
import sys
from pathlib import Path


INFRASTRUCTURE = (
    Path(__file__)
    .resolve()
    .parents[1]
)

sys.path.insert(
    0,
    str(INFRASTRUCTURE),
)

from policy_evaluate import evaluate_plan


def resource(
    address,
    resource_type,
    after,
):
    return {
        "address":
            address,
        "type":
            resource_type,
        "change": {
            "after":
                after,
        },
    }


def tags(zone, classification):
    return {
        "SecurityZone":
            zone,
        "DataClassification":
            classification,
    }


def baseline():
    return {
        "resource_changes": [
            resource(
                "aws_vpc.redoubt",
                "aws_vpc",
                {
                    "tags":
                        tags(
                            "core",
                            "INTERNAL",
                        ),
                },
            ),
            resource(
                "aws_subnet.application",
                "aws_subnet",
                {
                    "map_public_ip_on_launch":
                        False,
                    "tags":
                        tags(
                            "application",
                            "CONFIDENTIAL",
                        ),
                },
            ),
            resource(
                "aws_security_group.application",
                "aws_security_group",
                {
                    "tags":
                        tags(
                            "application",
                            "CONFIDENTIAL",
                        ),
                },
            ),
            resource(
                "aws_kms_key.evidence",
                "aws_kms_key",
                {
                    "enable_key_rotation":
                        True,
                    "tags":
                        tags(
                            "security",
                            "RESTRICTED",
                        ),
                },
            ),
            resource(
                "aws_s3_bucket.evidence",
                "aws_s3_bucket",
                {
                    "tags":
                        tags(
                            "security",
                            "RESTRICTED",
                        ),
                },
            ),
            resource(
                "aws_s3_bucket_public_access_block.evidence",
                "aws_s3_bucket_public_access_block",
                {
                    "block_public_acls":
                        True,
                    "block_public_policy":
                        True,
                    "ignore_public_acls":
                        True,
                    "restrict_public_buckets":
                        True,
                },
            ),
            resource(
                "aws_s3_bucket_server_side_encryption_configuration.evidence",
                "aws_s3_bucket_server_side_encryption_configuration",
                {
                    "rule": [
                        {
                            "apply_server_side_encryption_by_default": [
                                {
                                    "sse_algorithm":
                                        "aws:kms",
                                }
                            ],
                        }
                    ],
                },
            ),
            resource(
                "aws_s3_bucket_versioning.evidence",
                "aws_s3_bucket_versioning",
                {
                    "versioning_configuration": [
                        {
                            "status":
                                "Enabled",
                        }
                    ],
                },
            ),
            resource(
                "aws_flow_log.redoubt",
                "aws_flow_log",
                {
                    "traffic_type":
                        "ALL",
                    "tags":
                        tags(
                            "telemetry",
                            "RESTRICTED",
                        ),
                },
            ),
        ]
    }


def ids(plan):
    return {
        item["id"]
        for item in evaluate_plan(
            plan
        )
    }


def expect_allow(name, plan):
    violations = evaluate_plan(
        plan
    )

    if violations:
        raise AssertionError(
            f"{name}: expected ALLOW, "
            f"received {violations}"
        )

    print(
        f"[PASS] {name}"
    )


def expect_deny(
    name,
    policy_id,
    plan,
):
    detected = ids(
        plan
    )

    if policy_id not in detected:
        raise AssertionError(
            f"{name}: expected {policy_id}, "
            f"received {sorted(detected)}"
        )

    print(
        f"[PASS] {policy_id} {name}"
    )


plan = baseline()

expect_allow(
    "compliant reference architecture",
    plan,
)


case = copy.deepcopy(
    plan
)

case["resource_changes"].append(
    resource(
        "aws_vpc_security_group_ingress_rule.bad_http",
        "aws_vpc_security_group_ingress_rule",
        {
            "cidr_ipv4":
                "0.0.0.0/0",
            "from_port":
                80,
            "to_port":
                80,
            "ip_protocol":
                "tcp",
        },
    )
)

expect_deny(
    "non-HTTPS Internet ingress",
    "IAC-001",
    case,
)


case = copy.deepcopy(
    plan
)

case["resource_changes"].append(
    resource(
        "aws_vpc_security_group_ingress_rule.public_ssh",
        "aws_vpc_security_group_ingress_rule",
        {
            "cidr_ipv4":
                "0.0.0.0/0",
            "from_port":
                22,
            "to_port":
                22,
            "ip_protocol":
                "tcp",
        },
    )
)

expect_deny(
    "public SSH exposure",
    "IAC-002",
    case,
)


case = copy.deepcopy(
    plan
)

case[
    "resource_changes"
][1][
    "change"
][
    "after"
][
    "map_public_ip_on_launch"
] = True

expect_deny(
    "public IP assignment in private zone",
    "IAC-003",
    case,
)


case = copy.deepcopy(
    plan
)

case["resource_changes"].append(
    resource(
        "aws_route.management_internet",
        "aws_route",
        {
            "destination_cidr_block":
                "0.0.0.0/0",
        },
    )
)

expect_deny(
    "default route outside edge zone",
    "IAC-004",
    case,
)


case = copy.deepcopy(
    plan
)

public_block = (
    case[
        "resource_changes"
    ][5][
        "change"
    ][
        "after"
    ]
)

public_block[
    "block_public_policy"
] = False

expect_deny(
    "evidence public-access protection disabled",
    "IAC-005",
    case,
)


case = copy.deepcopy(
    plan
)

encryption = (
    case[
        "resource_changes"
    ][6][
        "change"
    ][
        "after"
    ][
        "rule"
    ][0][
        "apply_server_side_encryption_by_default"
    ][0]
)

encryption[
    "sse_algorithm"
] = "AES256"

expect_deny(
    "evidence encryption downgraded",
    "IAC-006",
    case,
)


case = copy.deepcopy(
    plan
)

case[
    "resource_changes"
][7][
    "change"
][
    "after"
][
    "versioning_configuration"
][0][
    "status"
] = "Suspended"

expect_deny(
    "evidence versioning disabled",
    "IAC-007",
    case,
)


case = copy.deepcopy(
    plan
)

case[
    "resource_changes"
][3][
    "change"
][
    "after"
][
    "enable_key_rotation"
] = False

expect_deny(
    "KMS rotation disabled",
    "IAC-008",
    case,
)


case = copy.deepcopy(
    plan
)

case[
    "resource_changes"
][8][
    "change"
][
    "after"
][
    "traffic_type"
] = "ACCEPT"

expect_deny(
    "incomplete VPC flow telemetry",
    "IAC-009",
    case,
)


case = copy.deepcopy(
    plan
)

del case[
    "resource_changes"
][2][
    "change"
][
    "after"
][
    "tags"
][
    "DataClassification"
]

expect_deny(
    "security classification tag removed",
    "IAC-010",
    case,
)


case = copy.deepcopy(
    plan
)

case["resource_changes"].append(
    resource(
        "aws_vpc_security_group_egress_rule.unrestricted",
        "aws_vpc_security_group_egress_rule",
        {
            "cidr_ipv4":
                "0.0.0.0/0",
            "from_port":
                0,
            "to_port":
                65535,
            "ip_protocol":
                "tcp",
        },
    )
)

expect_deny(
    "unrestricted Internet egress",
    "IAC-011",
    case,
)


print()
print(
    "==============================================="
)
print(
    " PHASE 11 POLICY-AS-CODE TESTS: PASS"
)
print(
    "==============================================="
)
