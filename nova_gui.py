#!/usr/bin/env python3
"""Compatibility entry point for the former NOVA desktop console."""
from framezero_gui import build_engine_args, build_validation_args, main

__all__ = ["build_engine_args", "build_validation_args", "main"]

if __name__ == "__main__":
    raise SystemExit(main())
