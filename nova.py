#!/usr/bin/env python3
"""Compatibility entry point for installations that used the NOVA CLI."""
from framezero import main, parse_version, version_at_least

__all__ = ["main", "parse_version", "version_at_least"]

if __name__ == "__main__":
    raise SystemExit(main())
