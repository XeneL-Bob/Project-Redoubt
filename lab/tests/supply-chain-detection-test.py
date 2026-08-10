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
    12,
    0,
    tzinfo=timezone.utc,
)


# DET-013
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="release-verifier",
        event_type="release_verification",
        outcome="deny",
        subject="restech-release-component",
        resource="software-release",
        correlation_id="det013",
        details={
            "reason":
                "artifact_digest_mismatch",
        },
    )
)

assert "DET-013" in ids(alerts)

print(
    "[PASS] DET-013 artifact integrity failure"
)


# DET-014
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="release-verifier",
        event_type="release_verification",
        outcome="deny",
        subject="restech-release-component",
        resource="software-release",
        correlation_id="det014",
        details={
            "reason":
                "provenance_signature_invalid",
        },
    )
)

assert "DET-014" in ids(alerts)

print(
    "[PASS] DET-014 provenance signature failure"
)


# DET-015
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="release-verifier",
        event_type="release_verification",
        outcome="deny",
        subject="restech-release-component",
        resource="software-release",
        correlation_id="det015",
        details={
            "reason":
                "untrusted_builder_identity",
        },
    )
)

assert "DET-015" in ids(alerts)

print(
    "[PASS] DET-015 untrusted builder"
)


# DET-016
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="trusted-builder",
        event_type="build_decision",
        outcome="deny",
        subject="restech-release-component",
        resource="software-build",
        correlation_id="det016",
        details={
            "reason":
                "dirty_source",
        },
    )
)

assert "DET-016" in ids(alerts)

print(
    "[PASS] DET-016 dirty source build"
)


# DET-017
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="release-verifier",
        event_type="release_verification",
        outcome="deny",
        subject="restech-release-component",
        resource="software-release",
        correlation_id="det017",
        details={
            "reason":
                "provenance_signature_missing",
        },
    )
)

assert "DET-017" in ids(alerts)

print(
    "[PASS] DET-017 unsigned release"
)


# Legitimate trusted build suppresses DET-018
engine = DetectionEngine(RULES)

alerts = []

alerts.extend(
    engine.process_event(
        event(
            timestamp=base,
            source="trusted-builder",
            event_type="build_decision",
            outcome="allow",
            subject="restech-release-component",
            resource="software-build",
            correlation_id="legitimate-release",
            details={
                "builder":
                    "project-redoubt/trusted-builder",
            },
        )
    )
)

alerts.extend(
    engine.process_event(
        event(
            timestamp=(
                base
                + timedelta(seconds=2)
            ),
            source="release-verifier",
            event_type="release_verification",
            outcome="allow",
            subject="restech-release-component",
            resource="software-release",
            correlation_id="legitimate-release",
            details={
                "builder":
                    "project-redoubt/trusted-builder",
            },
        )
    )
)

assert "DET-018" not in ids(alerts)

print(
    "[PASS] Legitimate trusted build correlation suppressed"
)


# DET-018
engine = DetectionEngine(RULES)

alerts = engine.process_event(
    event(
        timestamp=base,
        source="release-verifier",
        event_type="release_verification",
        outcome="allow",
        subject="restech-release-component",
        resource="software-release",
        correlation_id="det018-bypass",
        details={
            "synthetic":
                True,
        },
    )
)

assert "DET-018" in ids(alerts)

print(
    "[PASS] DET-018 release without trusted build"
)


print()
print(
    "PHASE 10 SUPPLY CHAIN DETECTION UNIT TESTS: PASS"
)
