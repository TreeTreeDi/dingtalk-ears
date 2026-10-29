#!/usr/bin/env python3
"""Run all project checks using the active development Python environment."""
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="Apply safe lint fixes and format first")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    paths = ["backend", "tests", "scripts", "ears.py"]
    commands = []
    if args.fix:
        commands += [
            [sys.executable, "-m", "ruff", "check", "--fix"] + paths,
            [sys.executable, "-m", "black"] + paths,
            ["npm", "run", "lint:css:fix"],
            ["npm", "run", "format"],
        ]
    commands += [
        [sys.executable, "-m", "ruff", "check"] + paths,
        [sys.executable, "-m", "black", "--check"] + paths,
        ["npm", "run", "check"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
    ]
    for command in commands:
        print(" ".join(command), flush=True)
        subprocess.run(command, cwd=str(root), check=True)


if __name__ == "__main__":
    main()
