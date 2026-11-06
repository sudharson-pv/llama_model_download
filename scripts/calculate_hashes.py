#!/usr/bin/env python3
"""
calculate_hashes.py — Calculates SHA-256 and byte sizes for model artifacts.
Used in the LearnMate AI model distribution pipeline.
"""
import hashlib
import sys
from pathlib import Path

def calculate_sha256(filepath: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size

def main():
    if len(sys.argv) < 2:
        print("Usage: python calculate_hashes.py <file1> [file2...]")
        sys.exit(1)

    print(f"{'Filename':<35} {'Size (Bytes)':<15} {'SHA-256 Checksum'}")
    print("-" * 120)
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.is_file():
            print(f"{p.name:<35} NOT FOUND")
            continue
        digest, size = calculate_sha256(p)
        print(f"{p.name:<35} {size:<15} {digest}")

if __name__ == "__main__":
    main()
