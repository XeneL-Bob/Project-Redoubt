#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import tempfile
import time
import uuid

from datetime import datetime, timezone
from pathlib import Path


LAB = Path(__file__).resolve().parents[1]
ROOT = LAB.parent

SOURCE = LAB / "supply-chain" / "source"
POLICY = LAB / "supply-chain" / "policy"
SPOOL = (
    LAB
    / "supply-chain"
    / "runtime"
    / "telemetry"
)

ALERTS = (
    ROOT
    / "evidence"
    / "runtime"
    / "security-alerts.jsonl"
)

RESULTS = (
    ROOT
    / "evidence"
    / "runtime"
    / "adversary-results.jsonl"
)

BUILDER_IMAGE = (
    "project-redoubt-supply-builder"
)

SIGNER_IMAGE = (
    "project-redoubt-supply-signer"
)

VERIFIER_IMAGE = (
    "project-redoubt-supply-verifier"
)

APPROVER_IMAGE = (
    "project-redoubt-release-approver"
)

DEPLOYER_IMAGE = (
    "project-redoubt-deployer"
)

HOST_UID = str(os.getuid())
HOST_GID = str(os.getgid())

COMPOSE = [
    "docker",
    "compose",
    "--env-file",
    str(LAB / ".env"),
    "-f",
    str(LAB / "compose.yaml"),
]

PHASE10_SCENARIOS = {
    f"ADV-{number:03d}"
    for number in range(10, 17)
}

failures = 0


def run(
    command,
    *,
    check=False,
):
    return subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=check,
    )


def git(*args):
    result = run(
        [
            "git",
            "-C",
            str(ROOT),
            *args,
        ],
        check=True,
    )

    return result.stdout.strip()


SOURCE_COMMIT = git(
    "rev-parse",
    "HEAD",
)

SOURCE_BRANCH = git(
    "branch",
    "--show-current",
)

if SOURCE_BRANCH:
    SOURCE_REF = (
        f"refs/heads/{SOURCE_BRANCH}"
    )
else:
    SOURCE_REF = (
        f"detached/{SOURCE_COMMIT}"
    )


def combined_output(proc):
    return (
        proc.stdout
        + "\n"
        + proc.stderr
    ).strip()


def alert_offset():
    if not ALERTS.exists():
        return 0

    return len(
        ALERTS.read_text(
            encoding="utf-8"
        ).splitlines()
    )


def wait_alert(
    offset,
    detection_id,
    correlation,
):
    deadline = time.time() + 30

    while time.time() < deadline:

        if ALERTS.exists():

            lines = (
                ALERTS.read_text(
                    encoding="utf-8"
                )
                .splitlines()[offset:]
            )

            for line in lines:

                try:
                    alert = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if (
                    alert.get("detection_id")
                    != detection_id
                ):
                    continue

                if (
                    alert.get("correlation_id")
                    != correlation
                ):
                    continue

                return True

        time.sleep(1)

    return False


def service_running(service):
    proc = run(
        COMPOSE
        + [
            "ps",
            "-q",
            service,
        ]
    )

    container_id = proc.stdout.strip()

    if not container_id:
        return False

    proc = run(
        [
            "docker",
            "inspect",
            "-f",
            "{{.State.Running}}",
            container_id,
        ]
    )

    return (
        proc.returncode == 0
        and proc.stdout.strip()
        == "true"
    )


def ensure_images():
    builds = [
        (
            BUILDER_IMAGE,
            LAB
            / "supply-chain"
            / "builder",
        ),
        (
            SIGNER_IMAGE,
            LAB
            / "supply-chain"
            / "signer",
        ),
        (
            VERIFIER_IMAGE,
            LAB
            / "supply-chain"
            / "verifier",
        ),
        (
            APPROVER_IMAGE,
            LAB
            / "supply-chain"
            / "approver",
        ),
        (
            DEPLOYER_IMAGE,
            LAB
            / "supply-chain"
            / "deployer",
        ),
    ]

    for image, context in builds:

        proc = subprocess.run(
            [
                "docker",
                "build",
                "-q",
                "-t",
                image,
                str(context),
            ],
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=False,
        )

        if proc.returncode != 0:
            print(
                f"[FAIL] Unable to build {image}"
            )

            print(proc.stderr)

            raise SystemExit(1)


def new_runtime(path):
    for directory in (
        path / "private",
        path / "trust",
        path / "out",
        path / "receipt",
        path / "approval-private",
        path / "approval-trust",
        path / "approval",
        path / "deploy",
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


def generate_keys(runtime):
    return run(
        [
            "docker",
            "run",
            "--rm",
            "--network",
            "none",
            "--user",
            f"{HOST_UID}:{HOST_GID}",
            "-v",
            (
                f"{runtime / 'private'}:"
                "/private"
            ),
            "-v",
            (
                f"{runtime / 'trust'}:"
                "/trust"
            ),
            SIGNER_IMAGE,
            "python",
            "/app/keygen.py",
        ]
    )


def build_artifact(
    runtime,
    *,
    dirty=False,
    builder=(
        "project-redoubt/trusted-builder"
    ),
    correlation=None,
    telemetry=False,
):
    command = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--user",
        f"{HOST_UID}:{HOST_GID}",
        "-e",
        f"SOURCE_COMMIT={SOURCE_COMMIT}",
        "-e",
        f"SOURCE_REF={SOURCE_REF}",
        "-e",
        (
            "SOURCE_DIRTY=true"
            if dirty
            else "SOURCE_DIRTY=false"
        ),
        "-e",
        f"BUILDER_ID={builder}",
    ]

    if telemetry:
        command += [
            "-e",
            (
                "EVENTS_FILE="
                "/telemetry/security-events.jsonl"
            ),
            "-e",
            (
                "CORRELATION_ID="
                f"{correlation}"
            ),
            "-v",
            f"{SPOOL}:/telemetry",
        ]

    command += [
        "-v",
        f"{SOURCE}:/source:ro",
        "-v",
        f"{runtime / 'out'}:/out",
        BUILDER_IMAGE,
    ]

    return run(command)


def sign_provenance(runtime):
    return run(
        [
            "docker",
            "run",
            "--rm",
            "--network",
            "none",
            "--user",
            f"{HOST_UID}:{HOST_GID}",
            "-v",
            (
                f"{runtime / 'private'}:"
                "/private:ro"
            ),
            "-v",
            f"{runtime / 'out'}:/out",
            SIGNER_IMAGE,
            "python",
            "/app/sign.py",
        ]
    )


def verify_release(
    runtime,
    *,
    correlation=None,
    telemetry=False,
    receipt=False,
):
    command = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--user",
        f"{HOST_UID}:{HOST_GID}",
    ]

    if telemetry:
        command += [
            "-e",
            (
                "EVENTS_FILE="
                "/telemetry/security-events.jsonl"
            ),
            "-e",
            (
                "CORRELATION_ID="
                f"{correlation}"
            ),
            "-v",
            f"{SPOOL}:/telemetry",
        ]

    if receipt:
        command += [
            "-e",
            (
                "RECEIPT_FILE="
                "/receipt/verification-receipt.json"
            ),
            "-v",
            f"{runtime / 'receipt'}:/receipt",
        ]

    command += [
        "-v",
        f"{runtime / 'out'}:/out:ro",
        "-v",
        (
            f"{runtime / 'trust'}:"
            "/trust:ro"
        ),
        "-v",
        f"{POLICY}:/policy:ro",
        VERIFIER_IMAGE,
    ]

    return run(command)


def prepare_signed_release(
    runtime,
    *,
    builder=(
        "project-redoubt/trusted-builder"
    ),
    correlation=None,
):
    new_runtime(runtime)

    proc = generate_keys(runtime)

    if proc.returncode != 0:
        raise RuntimeError(
            combined_output(proc)
        )

    proc = build_artifact(
        runtime,
        builder=builder,
        correlation=correlation,
    )

    if proc.returncode != 0:
        raise RuntimeError(
            combined_output(proc)
        )

    proc = sign_provenance(runtime)

    if proc.returncode != 0:
        raise RuntimeError(
            combined_output(proc)
        )


def generate_approval_keys(
    runtime,
):
    return run(
        [
            "docker",
            "run",
            "--rm",
            "--network",
            "none",
            "--user",
            f"{HOST_UID}:{HOST_GID}",
            "-v",
            (
                f"{runtime / 'approval-private'}:"
                "/approval-private"
            ),
            "-v",
            (
                f"{runtime / 'approval-trust'}:"
                "/approval-trust"
            ),
            APPROVER_IMAGE,
            "python",
            "/app/keygen.py",
        ]
    )


def approve_release(
    runtime,
    *,
    correlation,
    telemetry=True,
):
    command = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--user",
        f"{HOST_UID}:{HOST_GID}",
        "-e",
        "APPROVER_ID=restech/release-approver",
        "-e",
        "DEPLOYMENT_ENVIRONMENT=staging",
        "-e",
        f"CORRELATION_ID={correlation}",
    ]

    if telemetry:
        command += [
            "-e",
            (
                "EVENTS_FILE="
                "/telemetry/security-events.jsonl"
            ),
            "-v",
            f"{SPOOL}:/telemetry",
        ]

    command += [
        "-v",
        f"{runtime / 'out'}:/release:ro",
        "-v",
        (
            f"{runtime / 'trust'}:"
            "/release-trust:ro"
        ),
        "-v",
        (
            f"{runtime / 'receipt'}:"
            "/receipt:ro"
        ),
        "-v",
        f"{POLICY}:/policy:ro",
        "-v",
        (
            f"{runtime / 'approval-private'}:"
            "/approval-private:ro"
        ),
        "-v",
        (
            f"{runtime / 'approval'}:"
            "/approval"
        ),
        APPROVER_IMAGE,
    ]

    return run(command)


def deploy_release(
    runtime,
    *,
    correlation,
    telemetry=True,
):
    command = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--user",
        f"{HOST_UID}:{HOST_GID}",
        "-e",
        "DEPLOYMENT_ENVIRONMENT=staging",
        "-e",
        f"CORRELATION_ID={correlation}",
    ]

    if telemetry:
        command += [
            "-e",
            (
                "EVENTS_FILE="
                "/telemetry/security-events.jsonl"
            ),
            "-v",
            f"{SPOOL}:/telemetry",
        ]

    command += [
        "-v",
        f"{runtime / 'out'}:/release:ro",
        "-v",
        (
            f"{runtime / 'approval'}:"
            "/approval:ro"
        ),
        "-v",
        (
            f"{runtime / 'approval-trust'}:"
            "/approval-trust:ro"
        ),
        "-v",
        f"{runtime / 'deploy'}:/deploy",
        DEPLOYER_IMAGE,
    ]

    return run(command)


def prune_phase10_results():
    if not RESULTS.exists():
        return

    retained = []

    for line in RESULTS.read_text(
        encoding="utf-8"
    ).splitlines():

        if not line.strip():
            continue

        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue

        if (
            row.get("scenario_id")
            not in PHASE10_SCENARIOS
        ):
            retained.append(row)

    RESULTS.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with RESULTS.open(
        "w",
        encoding="utf-8",
    ) as handle:

        for row in retained:
            handle.write(
                json.dumps(
                    row,
                    sort_keys=True,
                )
                + "\n"
            )


def save(
    scenario_id,
    title,
    *,
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
        outcomes.append(
            "PREVENTED"
        )

    if detected:
        outcomes.append(
            "DETECTED"
        )

    if contained:
        outcomes.append(
            "CONTAINED"
        )

    verdict = (
        "+".join(outcomes)
        if outcomes
        else "MISSED"
    )

    record = {
        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),
        "scenario_id":
            scenario_id,
        "title":
            title,
        "attack_path":
            "AP-004",
        "risk_ids":
            ["R-006"],
        "preventive_control":
            control,
        "detection_id":
            detection_id,
        "expected":
            expected,
        "observed":
            observed,
        "prevented":
            prevented,
        "detected":
            detected,
        "contained":
            contained,
        "verdict":
            verdict,
        "validation":
            (
                "PASS"
                if passed
                else "FAIL"
            ),
        "notes":
            notes,
    }

    RESULTS.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with RESULTS.open(
        "a",
        encoding="utf-8",
    ) as handle:
        handle.write(
            json.dumps(
                record,
                sort_keys=True,
            )
            + "\n"
        )

    result = (
        "PASS"
        if passed
        else "FAIL"
    )

    print(
        f"[{result}] "
        f"{scenario_id} "
        f"{title}"
    )

    print(
        f"       {verdict} | "
        f"{observed}"
    )


def main():
    SPOOL.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "============================================================"
    )
    print(
        " PROJECT REDOUBT — AP-004 SUPPLY CHAIN ADVERSARY VALIDATION"
    )
    print(
        "============================================================"
    )

    print()
    print("[Preflight] Runtime services")

    for service in (
        "detection",
        "supply-chain-telemetry-relay",
    ):
        if not service_running(service):
            print(
                f"[FAIL] {service} is not running"
            )
            return 1

        print(
            f"[PASS] {service} running"
        )

    print()
    print("[Preflight] Supply-chain images")

    ensure_images()

    print(
        "[PASS] Builder, signer, verifier, approver and deployer images ready"
    )

    prune_phase10_results()

    with tempfile.TemporaryDirectory(
        prefix="project-redoubt-ap004."
    ) as temp:

        tmp = Path(temp)

        # ADV-010
        print()
        print(
            "[1] ADV-010 dirty-source build attempt"
        )

        runtime = tmp / "adv010"
        new_runtime(runtime)

        corr = (
            "adv010."
            + str(uuid.uuid4())
        )

        start = alert_offset()

        proc = build_artifact(
            runtime,
            dirty=True,
            correlation=corr,
            telemetry=True,
        )

        output = combined_output(proc)

        blocked = (
            proc.returncode != 0
            and (
                "source repository is dirty"
                in output
            )
        )

        detected = wait_alert(
            start,
            "DET-016",
            corr,
        )

        save(
            "ADV-010",
            (
                "Compromised developer attempts "
                "dirty-source build"
            ),
            control=(
                "Trusted builder clean-source policy"
            ),
            expected=(
                "Build denied + DET-016"
            ),
            observed=(
                "build denied"
                if blocked
                else output
            ),
            prevented=blocked,
            detected=detected,
            contained=blocked,
            passed=(
                blocked
                and detected
            ),
            detection_id="DET-016",
        )

        # ADV-011
        print()
        print(
            "[2] ADV-011 post-build artifact tampering"
        )

        runtime = tmp / "adv011"

        prepare_signed_release(
            runtime
        )

        artifact = (
            runtime
            / "out"
            / "restech-release-component.tar"
        )

        with artifact.open("ab") as handle:
            handle.write(
                b"\nATTACKER-TAMPERED\n"
            )

        corr = (
            "adv011."
            + str(uuid.uuid4())
        )

        start = alert_offset()

        proc = verify_release(
            runtime,
            correlation=corr,
            telemetry=True,
        )

        output = combined_output(proc)

        blocked = (
            proc.returncode != 0
            and (
                "artifact digest mismatch"
                in output
            )
        )

        detected = wait_alert(
            start,
            "DET-013",
            corr,
        )

        save(
            "ADV-011",
            "Post-build artifact tampering",
            control=(
                "SHA-256 artifact integrity "
                "verification"
            ),
            expected=(
                "Release denied + DET-013"
            ),
            observed=(
                "artifact digest mismatch"
                if blocked
                else output
            ),
            prevented=blocked,
            detected=detected,
            contained=blocked,
            passed=(
                blocked
                and detected
            ),
            detection_id="DET-013",
        )

        # ADV-012
        print()
        print(
            "[3] ADV-012 provenance forgery"
        )

        runtime = tmp / "adv012"

        prepare_signed_release(
            runtime
        )

        provenance = (
            runtime
            / "out"
            / "provenance.json"
        )

        data = json.loads(
            provenance.read_text(
                encoding="utf-8"
            )
        )

        data["builder"]["id"] = (
            "attacker/forged-builder"
        )

        provenance.write_text(
            json.dumps(
                data,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

        corr = (
            "adv012."
            + str(uuid.uuid4())
        )

        start = alert_offset()

        proc = verify_release(
            runtime,
            correlation=corr,
            telemetry=True,
        )

        output = combined_output(proc)

        blocked = (
            proc.returncode != 0
            and (
                "provenance signature invalid"
                in output
            )
        )

        detected = wait_alert(
            start,
            "DET-014",
            corr,
        )

        save(
            "ADV-012",
            "Forged release provenance",
            control=(
                "Ed25519 signed provenance"
            ),
            expected=(
                "Release denied + DET-014"
            ),
            observed=(
                "invalid provenance signature"
                if blocked
                else output
            ),
            prevented=blocked,
            detected=detected,
            contained=blocked,
            passed=(
                blocked
                and detected
            ),
            detection_id="DET-014",
        )

        # ADV-013
        print()
        print(
            "[4] ADV-013 untrusted builder"
        )

        runtime = tmp / "adv013"

        prepare_signed_release(
            runtime,
            builder=(
                "attacker/untrusted-builder"
            ),
        )

        corr = (
            "adv013."
            + str(uuid.uuid4())
        )

        start = alert_offset()

        proc = verify_release(
            runtime,
            correlation=corr,
            telemetry=True,
        )

        output = combined_output(proc)

        blocked = (
            proc.returncode != 0
            and (
                "untrusted builder identity"
                in output
            )
        )

        detected = wait_alert(
            start,
            "DET-015",
            corr,
        )

        save(
            "ADV-013",
            (
                "Signed artifact from "
                "untrusted builder"
            ),
            control=(
                "Release builder identity policy"
            ),
            expected=(
                "Release denied + DET-015"
            ),
            observed=(
                "untrusted builder rejected"
                if blocked
                else output
            ),
            prevented=blocked,
            detected=detected,
            contained=blocked,
            passed=(
                blocked
                and detected
            ),
            detection_id="DET-015",
            notes=(
                "Valid signing authority does not "
                "override required builder identity."
            ),
        )

        # ADV-014
        print()
        print(
            "[5] ADV-014 unsigned release"
        )

        runtime = tmp / "adv014"
        new_runtime(runtime)

        proc = generate_keys(
            runtime
        )

        if proc.returncode != 0:
            raise RuntimeError(
                combined_output(proc)
            )

        proc = build_artifact(
            runtime
        )

        if proc.returncode != 0:
            raise RuntimeError(
                combined_output(proc)
            )

        corr = (
            "adv014."
            + str(uuid.uuid4())
        )

        start = alert_offset()

        proc = verify_release(
            runtime,
            correlation=corr,
            telemetry=True,
        )

        output = combined_output(proc)

        blocked = (
            proc.returncode != 0
            and (
                "required object missing: "
                "provenance.sig"
                in output
            )
        )

        detected = wait_alert(
            start,
            "DET-017",
            corr,
        )

        save(
            "ADV-014",
            "Unsigned release attempt",
            control=(
                "Mandatory signed provenance"
            ),
            expected=(
                "Release denied + DET-017"
            ),
            observed=(
                "unsigned release rejected"
                if blocked
                else output
            ),
            prevented=blocked,
            detected=detected,
            contained=blocked,
            passed=(
                blocked
                and detected
            ),
            detection_id="DET-017",
        )

        # ADV-015
        print()
        print(
            "[6] ADV-015 trusted-build path bypass"
        )

        runtime = tmp / "adv015"

        build_correlation = (
            "adv015.build."
            + str(uuid.uuid4())
        )

        attack_correlation = (
            "adv015.bypass."
            + str(uuid.uuid4())
        )

        prepare_signed_release(
            runtime,
            correlation=build_correlation,
        )

        proc = generate_approval_keys(
            runtime
        )

        if proc.returncode != 0:
            raise RuntimeError(
                combined_output(proc)
            )

        start_det018 = alert_offset()

        proc = verify_release(
            runtime,
            correlation=attack_correlation,
            telemetry=True,
            receipt=True,
        )

        verifier_output = combined_output(
            proc
        )

        verifier_allowed = (
            proc.returncode == 0
            and (
                '"decision": "ALLOW"'
                in verifier_output
            )
        )

        det018 = wait_alert(
            start_det018,
            "DET-018",
            attack_correlation,
        )

        start_det019 = alert_offset()

        proc = approve_release(
            runtime,
            correlation=attack_correlation,
            telemetry=True,
        )

        approver_output = combined_output(
            proc
        )

        approval_denied = (
            proc.returncode != 0
            and (
                "trusted build correlation mismatch"
                in approver_output
            )
        )

        det019 = wait_alert(
            start_det019,
            "DET-019",
            attack_correlation,
        )

        approval_file = (
            runtime
            / "approval"
            / "deployment-approval.json"
        )

        no_approval_issued = (
            not approval_file.exists()
        )

        start_det020 = alert_offset()

        proc = deploy_release(
            runtime,
            correlation=attack_correlation,
            telemetry=True,
        )

        deployment_output = combined_output(
            proc
        )

        deployment_denied = (
            proc.returncode != 0
            and (
                "required object missing"
                in deployment_output
            )
        )

        det020 = wait_alert(
            start_det020,
            "DET-020",
            attack_correlation,
        )

        prevented = (
            approval_denied
            and no_approval_issued
            and deployment_denied
        )

        detected = (
            det018
            and det019
            and det020
        )

        contained = (
            no_approval_issued
            and deployment_denied
        )

        save(
            "ADV-015",
            (
                "Trusted-build path bypass "
                "against deployment boundary"
            ),
            control=(
                "Trusted-build correlation + "
                "independent deployment approval gate"
            ),
            expected=(
                "DET-018 + approval DENY + "
                "DET-019 + deployment DENY + DET-020"
            ),
            observed=(
                "release anomaly detected; "
                "approval denied; "
                "deployment denied"
                if (
                    verifier_allowed
                    and prevented
                    and detected
                )
                else (
                    "verifier="
                    f"{verifier_output}; "
                    "approver="
                    f"{approver_output}; "
                    "deployment="
                    f"{deployment_output}"
                )
            ),
            prevented=prevented,
            detected=detected,
            contained=contained,
            passed=(
                verifier_allowed
                and prevented
                and detected
                and contained
            ),
            detection_id=(
                "DET-018/DET-019/DET-020"
            ),
            notes=(
                "The verifier ALLOW alone is no longer "
                "sufficient for deployment. The independent "
                "approver requires matching trusted-build "
                "correlation and the deployment gate requires "
                "a valid signed approval."
            ),
        )

        # ADV-016
        print()
        print(
            "[7] ADV-016 signing-key isolation"
        )

        code = (
            "from pathlib import Path; "
            "key=Path("
            "'/private/release-signing-key.pem'"
            "); "
            "print("
            "'KEY_PRESENT' "
            "if key.exists() "
            "else 'KEY_ISOLATED'"
            "); "
            "raise SystemExit("
            "2 if key.exists() else 0"
            ")"
        )

        proc = run(
            [
                "docker",
                "run",
                "--rm",
                "--network",
                "none",
                "--entrypoint",
                "python",
                "-v",
                f"{SOURCE}:/source:ro",
                BUILDER_IMAGE,
                "-c",
                code,
            ]
        )

        isolated = (
            proc.returncode == 0
            and (
                "KEY_ISOLATED"
                in proc.stdout
            )
        )

        save(
            "ADV-016",
            (
                "Compromised build context attempts "
                "release signing-key access"
            ),
            control=(
                "Builder and signer trust-domain separation"
            ),
            expected=(
                "Release private key unavailable"
            ),
            observed=(
                proc.stdout.strip()
                or proc.stderr.strip()
            ),
            prevented=isolated,
            detected=False,
            contained=isolated,
            passed=isolated,
            notes=(
                "The trusted builder receives no "
                "release-signing private key."
            ),
        )

    print()
    print(
        "============================================================"
    )

    if failures:
        print(
            " PHASE 10 AP-004 ADVERSARY VALIDATION: "
            f"FAIL ({failures})"
        )
        print(
            "============================================================"
        )

        return 1

    print(
        " PHASE 10 AP-004 ADVERSARY VALIDATION: PASS"
    )
    print(
        "============================================================"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
