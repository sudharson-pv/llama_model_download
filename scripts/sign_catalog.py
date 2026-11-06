#!/usr/bin/env python3
"""
sign_catalog.py — Signs the catalog.json file using Ed25519.
Produces catalog.sig containing the Base64-encoded signature.
"""
import base64
import json
import sys
from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_der_public_key

OFFICIAL_PUBLISHER_KEY_BASE64 = "MCowBQYDK2VwAyEAN77dwAlm5tC1Nzatm0F/6jbLXvdXmDZw8tXbsNaWl+A="

def canonical_catalog_bytes(catalog_data: dict) -> bytes:
    # Deterministic JSON serialization
    return json.dumps(catalog_data, sort_keys=True, separators=(',', ':')).encode('utf-8')

def main():
    if len(sys.argv) < 3:
        print("Usage: python sign_catalog.py <catalog.json> <private_key.pem> [catalog.sig]")
        sys.exit(1)

    catalog_path = Path(sys.argv[1])
    key_path = Path(sys.argv[2])
    sig_out = Path(sys.argv[3]) if len(sys.argv) >= 4 else catalog_path.with_suffix(".sig")

    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(key_path, "rb") as f:
        key_pem = f.read()

    payload = canonical_catalog_bytes(data)
    key = load_pem_private_key(key_pem, password=None)
    sig_bytes = key.sign(payload)
    sig_b64 = base64.b64encode(sig_bytes).decode("utf-8")

    # Verify self
    pub_der = base64.b64decode(OFFICIAL_PUBLISHER_KEY_BASE64)
    pub = load_der_public_key(pub_der)
    pub.verify(sig_bytes, payload)

    with open(sig_out, "w", encoding="utf-8") as f:
        f.write(sig_b64 + "\n")

    print(f"Catalog successfully signed ({len(payload)} bytes payload).")
    print(f"Signature (Base64): {sig_b64}")
    print(f"Written signature to {sig_out.name}")

if __name__ == "__main__":
    main()
