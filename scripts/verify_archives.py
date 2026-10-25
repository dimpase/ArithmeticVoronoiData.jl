"""Check imported data and LFS payloads against their original SHA-256 hashes."""
import hashlib
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def verify():
    provenance = json.loads((ROOT / "provenance/import.json").read_text())
    imported = [item for item in provenance["files"]
                if item["path"].startswith(("data/", "archives/"))]
    for item in imported:
        path = ROOT / item["path"]
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if path.stat().st_size != item["bytes"] or digest != item["sha256"]:
            raise ValueError(f"Import checksum mismatch: {path}; run git lfs pull for missing archive payloads")

    for manifest_path in (ROOT / "archives/dataset/archive_manifest.json",
                          ROOT / "archives/fixtures/two_cells_v1.json"):
        manifest = json.loads(manifest_path.read_text())
        archive = manifest_path.parent / manifest["archive"]
        with archive.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if archive.stat().st_size != manifest["bytes"] or digest != manifest["sha256"]:
            raise ValueError(f"Archive manifest mismatch: {archive}")
        if "files" in manifest:
            with tarfile.open(archive) as source:
                members = source.getmembers()
                if len(members) != len(manifest["files"]) or {m.name for m in members} != set(manifest["files"]):
                    raise ValueError("Fixture archive members do not match the manifest")
                for member in members:
                    if not member.isfile():
                        raise ValueError(f"Unexpected fixture member: {member.name}")
                    with source.extractfile(member) as stream:
                        digest = hashlib.file_digest(stream, "sha256").hexdigest()
                    if digest != manifest["files"][member.name]:
                        raise ValueError(f"Fixture checksum mismatch: {member.name}")
    print(f"Verified {len(imported)} imported data files, both archives and every regression fixture")


if __name__ == "__main__":
    verify()
