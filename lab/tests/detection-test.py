import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(LAB_DIR / "detection"),
)

from engine import DetectionEngine, load_rules


RULES = load_rules(
    LAB_DIR / "detection" / "rules.json"
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
        "timestamp": timestamp.isoformat(),
        "source": source,
        "event_type": event_type,
        "outcome": outcome,
        "subject": subject,
        "resource": resource,
        "correlation_id": correlation_id,
        "details": details or {},
    }


def detection_ids(alerts):
    return {
        alert["detection_id"]
        for alert in alerts
    }


base = datetime(
    2026,
    8,
    10,
    9,
    0,
    tzinfo=timezone.utc,
)


# DET-001
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="gateway",
        event_type="policy_decision",
        outcome="deny",
        subject="alice.employee",
        resource="finance-api",
        correlation_id="det001",
        details={
            "device_trusted": True
        },
    )
)

assert "DET-001" in detection_ids(alerts)

print(
    "[PASS] DET-001 restricted Finance denial"
)


# DET-002
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="gateway",
        event_type="policy_decision",
        outcome="deny",
        subject="carol.finance",
        resource="finance-api",
        correlation_id="det002",
        details={
            "device_trusted": False
        },
    )
)

assert "DET-002" in detection_ids(alerts)

print(
    "[PASS] DET-002 untrusted-device Finance attempt"
)


# DET-003
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
                source="gateway",
                event_type="policy_decision",
                outcome="deny",
                subject="bob.developer",
                resource="finance-api",
                correlation_id=f"det003-{i}",
                details={
                    "device_trusted": True
                },
            )
        )
    )

assert "DET-003" in detection_ids(alerts)

print(
    "[PASS] DET-003 repeated authorisation denials"
)


# Legitimate Finance path
engine = DetectionEngine(RULES)

alerts = []

alerts.extend(
    engine.process_event(
        event(
            timestamp=base,
            source="gateway",
            event_type="policy_decision",
            outcome="allow",
            subject="carol.finance",
            resource="finance-api",
            correlation_id="legitimate",
            details={
                "device_trusted": True
            },
        )
    )
)

alerts.extend(
    engine.process_event(
        event(
            timestamp=base + timedelta(seconds=1),
            source="finance-api",
            event_type="vault_secret_access",
            outcome="allow",
            subject="carol.finance",
            resource="finance-api",
            correlation_id="legitimate",
        )
    )
)

alerts.extend(
    engine.process_event(
        event(
            timestamp=base + timedelta(seconds=2),
            source="finance-api",
            event_type="application_access",
            outcome="allow",
            subject="carol.finance",
            resource="finance-api",
            correlation_id="legitimate",
        )
    )
)

ids = detection_ids(alerts)

assert "DET-004" not in ids
assert "DET-005" not in ids

print(
    "[PASS] Legitimate correlated Finance flow suppressed"
)


# DET-004
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="finance-api",
        event_type="application_access",
        outcome="allow",
        subject="phase6.synthetic",
        resource="finance-api",
        correlation_id="policy-bypass",
    )
)

assert "DET-004" in detection_ids(alerts)

print("[PASS] DET-004 policy bypass")


# DET-005
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="finance-api",
        event_type="vault_secret_access",
        outcome="allow",
        subject="phase6.synthetic",
        resource="finance-api",
        correlation_id="secret-bypass",
    )
)

assert "DET-005" in detection_ids(alerts)

print(
    "[PASS] DET-005 secret access without policy authorisation"
)


# DET-006
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="finance-api",
        event_type="direct_backend_access_denied",
        outcome="deny",
        subject="unknown",
        resource="finance-api",
        correlation_id="direct-backend",
    )
)

assert "DET-006" in detection_ids(alerts)

print(
    "[PASS] DET-006 direct backend access attempt"
)


print()
print(
    "PHASE 6 DETECTION UNIT TESTS: PASS"
)
