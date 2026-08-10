import sys

from datetime import (
    datetime,
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


def ids(alerts):
    return {
        alert["detection_id"]
        for alert in alerts
    }


def event(
    *,
    source,
    event_type,
    outcome,
    correlation_id,
    reason,
):
    return {
        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),
        "source":
            source,
        "event_type":
            event_type,
        "outcome":
            outcome,
        "subject":
            "phase10.test",
        "resource":
            "software-deployment",
        "correlation_id":
            correlation_id,
        "details": {
            "reason":
                reason,
        },
    }


engine = DetectionEngine(
    RULES
)

alerts = engine.process_event(
    event(
        source=
            "release-approver",
        event_type=
            "deployment_approval",
        outcome=
            "deny",
        correlation_id=
            "det019",
        reason=
            "trusted_build_correlation_mismatch",
    )
)

assert "DET-019" in ids(alerts)

print(
    "[PASS] DET-019 deployment approval denied"
)


engine = DetectionEngine(
    RULES
)

alerts = engine.process_event(
    event(
        source=
            "deployment-gate",
        event_type=
            "deployment_decision",
        outcome=
            "deny",
        correlation_id=
            "det020",
        reason=
            "artifact_differs_from_approved_release",
    )
)

assert "DET-020" in ids(alerts)

print(
    "[PASS] DET-020 deployment gate denied"
)


print()
print(
    "PHASE 10 DEPLOYMENT DETECTION UNIT TESTS: PASS"
)
