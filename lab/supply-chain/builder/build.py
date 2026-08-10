import hashlib
import json
import os
import tarfile
from pathlib import Path


SOURCE = Path("/source")
OUT = Path("/out")

ARTIFACT = OUT / "restech-release-component.tar"
PROVENANCE = OUT / "provenance.json"

BUILDER_ID = os.environ.get(
    "BUILDER_ID",
    "project-redoubt/trusted-builder",
)

SOURCE_COMMIT = os.environ.get("SOURCE_COMMIT", "")
SOURCE_REF = os.environ.get("SOURCE_REF", "")
SOURCE_DIRTY = os.environ.get("SOURCE_DIRTY", "true")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def add_deterministic(
    archive: tarfile.TarFile,
    path: Path,
    arcname: str,
) -> None:
    info = archive.gettarinfo(
        str(path),
        arcname=arcname,
    )

    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0

    with path.open("rb") as handle:
        archive.addfile(info, handle)


if SOURCE_DIRTY.lower() != "false":
    raise SystemExit(
        "BUILD DENIED: source repository is dirty"
    )

if not SOURCE_COMMIT:
    raise SystemExit(
        "BUILD DENIED: source commit is missing"
    )

if not SOURCE_REF:
    raise SystemExit(
        "BUILD DENIED: source ref is missing"
    )

OUT.mkdir(
    parents=True,
    exist_ok=True,
)

source_files = sorted(
    path
    for path in SOURCE.rglob("*")
    if path.is_file()
)

if not source_files:
    raise SystemExit(
        "BUILD DENIED: no source files found"
    )

with tarfile.open(
    ARTIFACT,
    mode="w",
) as archive:
    for path in source_files:
        relative = path.relative_to(SOURCE)

        add_deterministic(
            archive,
            path,
            str(relative),
        )

artifact_digest = sha256_file(ARTIFACT)

provenance = {
    "schema": "project-redoubt.provenance/v1",
    "artifact": {
        "name": ARTIFACT.name,
        "digest": {
            "algorithm": "sha256",
            "value": artifact_digest,
        },
    },
    "builder": {
        "id": BUILDER_ID,
    },
    "source": {
        "commit": SOURCE_COMMIT,
        "ref": SOURCE_REF,
        "dirty": False,
    },
}

PROVENANCE.write_text(
    json.dumps(
        provenance,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)

print(
    json.dumps(
        {
            "status": "built",
            "artifact": ARTIFACT.name,
            "sha256": artifact_digest,
            "builder": BUILDER_ID,
            "source_commit": SOURCE_COMMIT,
        },
        sort_keys=True,
    )
)
