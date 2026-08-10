import sys

from datetime import (
    datetime,
    timedelta,
    timezone,
)

from pathlib import Path


LAB_DIR = Path(
    __file__
).resolve().parents[1]

sys.path.insert(
    0,
    str(
        LAB_DIR
        / "detection"
    ),
)

from engine import (
    DetectionEngine,
    load_rules,
)


RULES = load_rules(
    LAB_DIR
    / "detection"
    / "rules.json"
)


def event(
    *,
    timestamp,
    source,
    event_type,
    outcome,
    subject,
    resource,
    correlation_id,
    details=None,
):
    return {
        "timestamp":
            timestamp.isoformat(),
        "source":
            source,
        "event_type":
            event_type,
        "outcome":
            outcome,
        "subject":
            subject,
        "resource":
            resource,
        "correlation_id":
            correlation_id,
        "details":
            details or {},
    }


def ids(alerts):
    return {
        alert["detection_id"]
        for alert in alerts
    }


base = datetime(
    2026,
    8,
    10,
    10,
    0,
    tzinfo=timezone.utc,
)


# DET-007
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="privilege-broker",
        event_type="privileged_elevation",
        outcome="deny",
        subject="alice.employee",
        resource="infrastructure",
        correlation_id="det007",
        details={
            "reason":
                "missing_privileged_role",
        },
    )
)

assert "DET-007" in ids(alerts)

print(
    "[PASS] DET-007 privileged elevation denied"
)


# DET-008
engine = DetectionEngine(RULES)
alerts = []

for i in range(3):
    alerts.extend(
        engine.process_event(
            event(
                timestamp=(
                    base
                    + timedelta(
                        seconds=i * 10
                    )
                ),
                source="privilege-broker",
                event_type="privileged_elevation",
                outcome="deny",
                subject="phase9.threshold",
                resource="infrastructure",
                correlation_id=f"det008-{i}",
            )
        )
    )

assert "DET-008" in ids(alerts)

print(
    "[PASS] DET-008 repeated privileged elevation denials"
)


# DET-009
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="management-api",
        event_type="direct_management_access_denied",
        outcome="deny",
        subject="attacker",
        resource="infrastructure-management",
        correlation_id="det009",
    )
)

assert "DET-009" in ids(alerts)

print(
    "[PASS] DET-009 direct management backend attempt"
)


# DET-010
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="management-gateway",
        event_type="privileged_policy_decision",
        outcome="deny",
        subject="ian.infrastructure",
        resource="infrastructure-management",
        correlation_id="det010",
        details={
            "admin_device_trusted":
                False,
            "elevation_active":
                True,
        },
    )
)

assert "DET-010" in ids(alerts)

print(
    "[PASS] DET-010 untrusted privileged device"
)


# DET-011
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="management-api",
        event_type="privileged_operation",
        outcome="allow",
        subject="sophie.security",
        resource="security-management",
        correlation_id="det011",
        details={
            "action":
                "update-detection",
        },
    )
)

alert_ids = ids(alerts)

assert "DET-011" in alert_ids
assert "DET-012" in alert_ids

print(
    "[PASS] DET-011 security-control modification"
)


# Legitimate management path suppresses DET-012
engine = DetectionEngine(RULES)

alerts = []

alerts.extend(
    engine.process_event(
        event(
            timestamp=base,
            source="management-gateway",
            event_type="privileged_policy_decision",
            outcome="allow",
            subject="ian.infrastructure",
            resource="infrastructure-management",
            correlation_id="legitimate-management",
            details={
                "admin_device_trusted":
                    True,
                "elevation_active":
                    True,
            },
        )
    )
)

alerts.extend(
    engine.process_event(
        event(
            timestamp=(
                base
                + timedelta(seconds=1)
            ),
            source="management-api",
            event_type="privileged_operation",
            outcome="allow",
            subject="ian.infrastructure",
            resource="infrastructure-management",
            correlation_id="legitimate-management",
            details={
                "action":
                    "read",
            },
        )
    )
)

assert "DET-012" not in ids(alerts)

print(
    "[PASS] Legitimate correlated management flow suppressed"
)


# DET-012
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="management-api",
        event_type="privileged_operation",
        outcome="allow",
        subject="phase9.synthetic",
        resource="security-management",
        correlation_id="det012",
        details={
            "action":
                "read",
            "synthetic":
                True,
        },
    )
)

assert "DET-012" in ids(alerts)

print(
    "[PASS] DET-012 management policy bypass"
)


print()
print(
    "PHASE 9 PRIVILEGED DETECTION UNIT TESTS: PASS"
)
