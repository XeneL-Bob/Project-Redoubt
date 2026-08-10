#!/usr/bin/env python3

import json
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

from datetime import datetime, timezone
from pathlib import Path


LAB = Path(__file__).resolve().parents[1]
ROOT = LAB.parent

ENV = {}

for raw in (LAB / ".env").read_text().splitlines():
    if "=" in raw and not raw.lstrip().startswith("#"):
        key, value = raw.split("=", 1)
        ENV[key] = value


EVENTS = ROOT / "evidence/runtime/security-events.jsonl"
ALERTS = ROOT / "evidence/runtime/security-alerts.jsonl"
RESULTS = ROOT / "evidence/runtime/adversary-results.jsonl"

KEYCLOAK = "http://localhost:8080"
GATEWAY = "http://localhost:8000"

COMPOSE = [
    "docker",
    "compose",
    "--env-file",
    str(LAB / ".env"),
    "-f",
    str(LAB / "compose.yaml"),
]

failures = 0


def request(url, headers=None, data=None):
    req = urllib.request.Request(
        url,
        headers=headers or {},
        data=data,
    )

    try:
        with urllib.request.urlopen(
            req,
            timeout=10,
        ) as response:
            return (
                response.status,
                response.read().decode(),
            )

    except urllib.error.HTTPError as exc:
        return (
            exc.code,
            exc.read().decode(),
        )


def token(username, password):
    data = urllib.parse.urlencode(
        {
            "client_id": "redoubt-test-cli",
            "username": username,
            "password": password,
            "grant_type": "password",
        }
    ).encode()

    status, body = request(
        f"{KEYCLOAK}/realms/restech/protocol/openid-connect/token",
        {
            "Content-Type":
                "application/x-www-form-urlencoded",
        },
        data,
    )

    if status != 200:
        raise RuntimeError(
            f"{username} authentication failed: "
            f"HTTP {status}"
        )

    return json.loads(body)["access_token"]


def gateway(path, access_token, trusted=True):
    status, _ = request(
        GATEWAY + path,
        {
            "Authorization":
                f"Bearer {access_token}",
            "X-Device-Trusted":
                "true" if trusted else "false",
        },
    )

    return status


def alert_offset():
    if not ALERTS.exists():
        return 0

    return len(
        ALERTS.read_text().splitlines()
    )


def wait_alert(
    offset,
    detection_id,
    subject=None,
    correlation=None,
):
    deadline = time.time() + 15

    while time.time() < deadline:
        if ALERTS.exists():
            lines = (
                ALERTS.read_text()
                .splitlines()[offset:]
            )

            for line in lines:
                alert = json.loads(line)

                if (
                    alert.get("detection_id")
                    != detection_id
                ):
                    continue

                if (
                    subject
                    and alert.get("subject")
                    != subject
                ):
                    continue

                if (
                    correlation
                    and alert.get("correlation_id")
                    != correlation
                ):
                    continue

                return True

        time.sleep(1)

    return False


def exec_python(service, code):
    return subprocess.run(
        COMPOSE
        + [
            "exec",
            "-T",
            service,
            "python",
            "-c",
            code,
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def inject(event):
    EVENTS.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with EVENTS.open("a") as handle:
        handle.write(
            json.dumps(
                event,
                sort_keys=True,
            )
            + "\n"
        )


def save(
    scenario_id,
    title,
    attack_path,
    risks,
    control,
    expected,
    observed,
    prevented,
    detected,
    contained,
    passed,
    detection_id=None,
    notes="",
):
    global failures

    if not passed:
        failures += 1

    outcomes = []

    if prevented:
        outcomes.append("PREVENTED")

    if detected:
        outcomes.append("DETECTED")

    if contained:
        outcomes.append("CONTAINED")

    verdict = (
        "+".join(outcomes)
        if outcomes
        else "MISSED"
    )

    row = {
        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),
        "scenario_id": scenario_id,
        "title": title,
        "attack_path": attack_path,
        "risk_ids": risks,
        "preventive_control": control,
        "detection_id": detection_id,
        "expected": expected,
        "observed": observed,
        "prevented": prevented,
        "detected": detected,
        "contained": contained,
        "verdict": verdict,
        "validation":
            "PASS" if passed else "FAIL",
        "notes": notes,
    }

    RESULTS.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with RESULTS.open("a") as handle:
        handle.write(
            json.dumps(
                row,
                sort_keys=True,
            )
            + "\n"
        )

    status = (
        "PASS"
        if passed
        else "FAIL"
    )

    print(
        f"[{status}] "
        f"{scenario_id} {title}"
    )

    print(
        f"       {verdict} | "
        f"{observed}"
    )


def main():
    RESULTS.unlink(
        missing_ok=True
    )

    alice = token(
        "alice.employee",
        ENV["ALICE_PASSWORD"],
    )

    bob = token(
        "bob.developer",
        ENV["BOB_PASSWORD"],
    )

    carol = token(
        "carol.finance",
        ENV["CAROL_PASSWORD"],
    )

    erin = token(
        "erin.contractor",
        ENV["ERIN_PASSWORD"],
    )

    print(
        "============================================================"
    )

    print(
        " PROJECT REDOUBT — PHASE 7 ADVERSARY VALIDATION"
    )

    print(
        "============================================================"
    )


    # ADV-001
    start = alert_offset()

    status = gateway(
        "/finance/summary",
        alice,
    )

    detected = wait_alert(
        start,
        "DET-001",
        "alice.employee",
    )

    save(
        "ADV-001",
        "Compromised employee attempts Finance access",
        "AP-001",
        ["R-001", "R-003"],
        "OPA least privilege",
        "HTTP 403 + DET-001",
        f"HTTP {status}",
        status == 403,
        detected,
        status == 403,
        status == 403 and detected,
        "DET-001",
    )


    # ADV-002
    start = alert_offset()

    status = gateway(
        "/finance/summary",
        carol,
        False,
    )

    detected = wait_alert(
        start,
        "DET-002",
        "carol.finance",
    )

    save(
        "ADV-002",
        "Finance identity from untrusted device",
        "AP-001",
        ["R-001", "R-005"],
        "Context-aware device trust",
        "HTTP 403 + DET-002",
        f"HTTP {status}",
        status == 403,
        detected,
        status == 403,
        status == 403 and detected,
        "DET-002",
    )


    # ADV-003
    #
    # Prevention is validated using the real developer identity.
    # Threshold detection uses a unique synthetic subject so the
    # scenario remains repeatable even when the detection engine
    # retains recent threshold state from previous test runs.

    codes = [
        gateway(
            "/finance/summary",
            bob,
        )
        for _ in range(3)
    ]

    denied = all(
        code == 403
        for code in codes
    )

    start = alert_offset()

    threshold_subject = (
        "phase7.repeated-denial."
        + str(uuid.uuid4())
    )

    now = datetime.now(
        timezone.utc
    ).isoformat()

    for index in range(3):
        inject(
            {
                "timestamp": now,
                "source": "gateway",
                "event_type": "policy_decision",
                "outcome": "deny",
                "subject": threshold_subject,
                "resource": "finance-api",
                "correlation_id": (
                    threshold_subject
                    + f"-{index}"
                ),
                "details": {
                    "synthetic": True,
                    "phase": 7,
                    "scenario": "ADV-003",
                },
            }
        )

    detected = wait_alert(
        start,
        "DET-003",
        threshold_subject,
    )

    save(
        "ADV-003",
        "Repeated developer privilege expansion",
        "AP-001",
        ["R-001", "R-003"],
        "Default-deny authorisation",
        "3 x HTTP 403 + DET-003",
        (
            f"developer HTTP codes={codes}; "
            f"threshold_subject={threshold_subject}"
        ),
        denied,
        detected,
        denied,
        denied and detected,
        "DET-003",
        (
            "Prevention validated using bob.developer; "
            "threshold detection validated using a unique "
            "synthetic denied subject to ensure repeatability."
        ),
    )


    # ADV-004
    status = gateway(
        "/employee/profile",
        erin,
    )

    save(
        "ADV-004",
        "Contractor scope escape",
        "AP-007",
        ["R-010"],
        "Role-based least privilege",
        "HTTP 403",
        f"HTTP {status}",
        status == 403,
        False,
        status == 403,
        status == 403,
    )


    # ADV-005
    lateral_code = '''
import socket

try:
    socket.getaddrinfo(
        "finance-api",
        8000,
    )

except socket.gaierror:
    print("ISOLATED")
    raise SystemExit(0)

print("REACHABLE")
raise SystemExit(2)
'''

    proc = exec_python(
        "employee-api",
        lateral_code,
    )

    isolated = (
        proc.returncode == 0
        and "ISOLATED"
        in proc.stdout
    )

    save(
        "ADV-005",
        "Employee workload lateral movement to Finance",
        "AP-001 / AP-003",
        ["R-003", "R-011"],
        "Application network segmentation",
        "Finance API not resolvable",
        proc.stdout.strip()
        or proc.stderr.strip(),
        isolated,
        False,
        isolated,
        isolated,
    )


    # ADV-006
    data_code = '''
import socket

try:
    socket.getaddrinfo(
        "finance-db",
        5432,
    )

except socket.gaierror:
    print("ISOLATED")
    raise SystemExit(0)

print("REACHABLE")
raise SystemExit(2)
'''

    proc = exec_python(
        "gateway",
        data_code,
    )

    isolated = (
        proc.returncode == 0
        and "ISOLATED"
        in proc.stdout
    )

    save(
        "ADV-006",
        "Gateway attempts direct Finance DB reachability",
        "AP-003",
        ["R-004", "R-011"],
        "Data-tier network segmentation",
        "Finance DB not resolvable",
        proc.stdout.strip()
        or proc.stderr.strip(),
        isolated,
        False,
        isolated,
        isolated,
    )


    # ADV-007
    start = alert_offset()

    corr = (
        "phase7-direct-"
        + str(uuid.uuid4())
    )

    direct_code = f'''
import urllib.error
import urllib.request

req = urllib.request.Request(
    "http://finance-api:8000/summary",
    headers={{
        "X-Redoubt-Gateway-Token":
            "invalid-phase7-token",
        "X-Redoubt-User":
            "phase7.direct-backend",
        "X-Redoubt-Correlation-ID":
            "{corr}",
    }},
)

try:
    urllib.request.urlopen(
        req,
        timeout=10,
    )

    print("HTTP 200")

except urllib.error.HTTPError as exc:
    print(f"HTTP {{exc.code}}")
'''

    proc = exec_python(
        "gateway",
        direct_code,
    )

    blocked = (
        "HTTP 403"
        in proc.stdout
    )

    detected = wait_alert(
        start,
        "DET-006",
        "phase7.direct-backend",
        corr,
    )

    save(
        "ADV-007",
        "Direct backend access with invalid workload credential",
        "AP-003",
        ["R-003", "R-011"],
        "Workload-specific gateway credential",
        "HTTP 403 + DET-006",
        proc.stdout.strip()
        or proc.stderr.strip(),
        blocked,
        detected,
        blocked,
        blocked and detected,
        "DET-006",
    )


    # ADV-008
    start = alert_offset()

    corr = (
        "phase7-policy-"
        + str(uuid.uuid4())
    )

    inject(
        {
            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),
            "source":
                "finance-api",
            "event_type":
                "application_access",
            "outcome":
                "allow",
            "subject":
                "phase7.synthetic-policy-bypass",
            "resource":
                "finance-api",
            "correlation_id":
                corr,
            "details": {
                "synthetic": True,
                "phase": 7,
            },
        }
    )

    detected = wait_alert(
        start,
        "DET-004",
        "phase7.synthetic-policy-bypass",
        corr,
    )

    save(
        "ADV-008",
        "Synthetic Finance policy-path bypass",
        "AP-003",
        ["R-004", "R-011"],
        "Detection validation injection",
        "DET-004",
        (
            "DET-004 generated"
            if detected
            else "No alert"
        ),
        False,
        detected,
        False,
        detected,
        "DET-004",
    )


    # ADV-009
    start = alert_offset()

    corr = (
        "phase7-secret-"
        + str(uuid.uuid4())
    )

    inject(
        {
            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),
            "source":
                "finance-api",
            "event_type":
                "vault_secret_access",
            "outcome":
                "allow",
            "subject":
                "phase7.synthetic-secret-bypass",
            "resource":
                "finance-api",
            "correlation_id":
                corr,
            "details": {
                "synthetic": True,
                "phase": 7,
            },
        }
    )

    detected = wait_alert(
        start,
        "DET-005",
        "phase7.synthetic-secret-bypass",
        corr,
    )

    save(
        "ADV-009",
        "Synthetic secret access without policy authorisation",
        "AP-003",
        ["R-007", "R-011"],
        "Detection validation injection",
        "DET-005",
        (
            "DET-005 generated"
            if detected
            else "No alert"
        ),
        False,
        detected,
        False,
        detected,
        "DET-005",
    )


    print(
        "============================================================"
    )

    if failures:
        print(
            " PHASE 7 ADVERSARY VALIDATION: "
            f"FAIL ({failures})"
        )

        return 1

    print(
        " PHASE 7 ADVERSARY VALIDATION: PASS"
    )

    print(
        "============================================================"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
