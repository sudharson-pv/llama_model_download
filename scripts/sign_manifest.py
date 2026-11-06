#!/usr/bin/env python3
"""
sign_manifest.py — Signs a model manifest or catalog with the LearnMate Ed25519 private key.
The private key is provided via command line or environment variable and is never committed to Git.
"""
import base64
import json
import os
import sys
from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from validate_manifest import canonical_serialize_manifest

def sign_payload(payload: bytes, private_key_pem: bytes) -> str:
    key = load_pem_private_key(private_key_pem, password=None)
    sig_bytes = key.sign(payload)
    return base64.b64encode(sig_bytes).decode("utf-8")

def main():
    if len(sys.argv) < 3:
        print("Usage: python sign_manifest.py <manifest.json> <private_key.pem> [output.sig]")
        sys.exit(1)

    manifest_path = Path(sys.argv[1])
    key_path = Path(sys.argv[2])
    sig_out = Path(sys.argv[3]) if len(sys.argv) >= 4 else manifest_path.with_suffix(".sig")

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(key_path, "rb") as f:
        key_pem = f.read()

    payload = canonical_serialize_manifest(data)
    sig_b64 = sign_payload(payload, key_pem)

    # Save standalone signature file
    with open(sig_out, "w", encoding="utf-8") as f:
        f.write(sig_b64 + "\n")

    # Also embed into manifest json
    data["signatureBase64"] = sig_b64
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully signed {manifest_path.name}")
    print(f"Signature (Base64): {sig_b64}")
    print(f"Written signature to {sig_out.name}")

if __name__ == "__main__":
    main()
