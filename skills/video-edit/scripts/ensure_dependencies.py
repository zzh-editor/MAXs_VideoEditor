#!/usr/bin/env python3
"""Check or install video-edit's upstream OpenCode skill dependencies."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


MANIFEST = Path(__file__).resolve().parents[1] / "references" / "dependencies.json"


def skill_roots(home=None, xdg_config_home=None):
    home = Path(home or Path.home())
    config_home = Path(xdg_config_home or os.environ.get("XDG_CONFIG_HOME", home / ".config"))
    return (config_home / "opencode" / "skills", home / ".agents" / "skills")


def missing_by_source(manifest, roots):
    missing = {}
    for source in manifest["sources"]:
        absent = [
            skill for skill in source["skills"]
            if not any((root / skill / "SKILL.md").is_file() for root in roots)
        ]
        if absent:
            missing[source["repository"]] = absent
    return missing


def install_command(repository, skills, agent="opencode"):
    return [
        "npx", "skills", "add", repository,
        "--global", "--agent", agent, "--skill", *skills, "--yes",
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="only report missing skills")
    parser.add_argument("--install-missing", action="store_true",
                        help="install missing skills globally with the skills CLI")
    args = parser.parse_args()
    if args.check and args.install_missing:
        parser.error("--check and --install-missing cannot be combined")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    roots = skill_roots()
    missing = missing_by_source(manifest, roots)
    if not missing:
        print("All video-edit skill dependencies are installed.")
        return 0

    for repository, skills in missing.items():
        print(f"Missing from {repository}: {', '.join(skills)}")
    if not args.install_missing:
        print("Run with --install-missing to install them globally.")
        return 1

    for repository, skills in missing.items():
        try:
            subprocess.run(install_command(repository, skills, manifest["agent"]), check=True)
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"Could not install {repository}: {exc}", file=sys.stderr)
            return 2

    missing = missing_by_source(manifest, roots)
    if missing:
        for repository, skills in missing.items():
            print(f"Still missing from {repository}: {', '.join(skills)}", file=sys.stderr)
        return 2
    print("All video-edit skill dependencies are installed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
