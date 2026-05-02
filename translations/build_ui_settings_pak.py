#!/usr/bin/env python3
"""Build ZZ_UISettingsRuPatch_P.pak from the current game's ui_settings asset."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GAME_PAK = REPO_ROOT.parent / "a09k/WindowsNoEditor/VotV/Content/Paks/VotV-WindowsNoEditor.pak"
UI_ASSET = "VotV/Content/umg/interfaces/ui_settings.uasset"
UI_UEXP = "VotV/Content/umg/interfaces/ui_settings.uexp"


def run(command: list[str], **kwargs) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, check=True, **kwargs)


def extract_file(game_pak: Path, name: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as f:
        run(["repak", "get", str(game_pak), name], stdout=f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build current-version UI settings Russian pak.")
    parser.add_argument("--game-pak", type=Path, default=DEFAULT_GAME_PAK, help="Path to VotV-WindowsNoEditor.pak")
    parser.add_argument(
        "--map",
        type=Path,
        default=REPO_ROOT / "translations/UI/ui_settings_map.json",
        help="Path to ui_settings_map.json",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=REPO_ROOT / "translations/output/ui_settings_current",
        help="Temporary build directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "ZZ_UISettingsRuPatch_P.pak",
        help="Output pak path",
    )
    parser.add_argument("--keep-work", action="store_true", help="Do not delete temporary extracted files")
    args = parser.parse_args()

    if not args.game_pak.exists():
        raise SystemExit(f"Game pak not found: {args.game_pak}")
    if not args.map.exists():
        raise SystemExit(f"Map not found: {args.map}")
    if shutil.which("repak") is None:
        raise SystemExit("repak is required in PATH")
    if shutil.which("cargo") is None:
        raise SystemExit("cargo is required in PATH")

    work = args.work_dir
    source = work / "source"
    patched = work / "patched"
    pakroot = work / "pakroot"
    shutil.rmtree(work, ignore_errors=True)

    source_uasset = source / "ui_settings.uasset"
    source_uexp = source / "ui_settings.uexp"
    patched_uasset = patched / UI_ASSET
    patched_uexp = patched / UI_UEXP

    extract_file(args.game_pak, UI_ASSET, source_uasset)
    extract_file(args.game_pak, UI_UEXP, source_uexp)

    run(
        [
            "cargo",
            "run",
            "--quiet",
            "--release",
            "--manifest-path",
            str(REPO_ROOT / "tools/ui_settings_patcher/Cargo.toml"),
            "--",
            str(source_uasset),
            str(source_uexp),
            str(args.map),
            str(patched_uasset),
            str(patched_uexp),
        ]
    )

    shutil.rmtree(pakroot, ignore_errors=True)
    for path in (patched_uasset, patched_uexp):
        target = pakroot / path.relative_to(patched)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "repak",
            "pack",
            "--version",
            "V11",
            "--path-hash-seed",
            "1476701736",
            "--mount-point",
            "../../../",
            str(pakroot),
            str(args.output),
        ]
    )

    if not args.keep_work:
        shutil.rmtree(work, ignore_errors=True)
    print(f"[INFO] Written {args.output}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
