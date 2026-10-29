#!/usr/bin/env python3
"""Compatibility launcher; implementation lives in the backend package."""
import sys

from backend.cli import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:] or ["run"]))
