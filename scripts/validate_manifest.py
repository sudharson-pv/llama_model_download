#!/usr/bin/env python3
"""
validate_manifest.py — Validates model manifests against canonical serialization
and verifies Ed25519 digital signatures against the official publisher public key.
"""
import base64
import json
import sys
from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_der_public_key

OFFICIAL_PUBLISHER_KEY_BASE64 = "MCowBQYDK2VwAyEAN77dwAlm5tC1Nzatm0F/6jbLXvdXmDZw8tXbsNaWl+A="

def canonical_serialize_manifest(data: dict) -> bytes:
    """
    Produces the deterministic newline-delimited key:value payload expected by LearnMate AI.
    """
    fields = [
        ("formatVersion", data.get("formatVersion", "1.0.0")),
        ("manifestVersion", data.get("manifestVersion", 1)),
        ("modelId", data.get("modelId", "")),
        ("modelVersion", data.get("modelVersion", "1.0.0")),
        ("modelFileName", data.get("modelFileName", "")),
        ("modelSizeBytes", data.get("modelSizeBytes", 0)),
        ("modelSha256", data.get("modelSha256", "").lower()),
        ("tokenizerFileName", data.get("tokenizerFileName", "")),
        ("tokenizerSizeBytes", data.get("tokenizerSizeBytes", 0)),
        ("tokenizerSha256", data.get("tokenizerSha256", "").lower()),
        ("format", data.get("format", "ExecuTorch PTE")),
        ("quantization", data.get("quantization", "")),
        ("targetBackend", data.get("targetBackend", "XNNPACK CPU")),
        ("minRuntimeVersion", data.get("minRuntimeVersion", "1.4.0")),
        ("minApiLevel", data.get("minApiLevel", 28)),
        ("minRamBytes", data.get("minRamBytes", 0)),
        ("minStorageBytes", data.get("minStorageBytes", 0)),
        ("license", data.get("license", "")),
        ("publisherKeyId", data.get("publisherKeyId", "learnmate_official_2026")),
        ("signatureTimestampEpochSec", data.get("signatureTimestampEpochSec", 0)),
        ("expiresTimestampEpochSec", data.get("expiresTimestampEpochSec", 0)),
    ]
    return "\n".join(f"{k}:{v}" for k, v in fields).encode("utf-8")

def verify_signature(payload: bytes, signature_base64: str) -> bool:
    try:
        pub_der = base64.b64decode(OFFICIAL_PUBLISHER_KEY_BASE64)
        public_key = load_der_public_key(pub_der)
        sig_bytes = base64.b64decode(signature_base64)
        public_key.verify(sig_bytes, payload)
        return True
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_manifest.py <manifest.json> [signature.sig]")
        sys.exit(1)

    manifest_path = Path(sys.argv[1])
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sig_b64 = None
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            sig_b64 = f.read().strip()
    elif "signatureBase64" in data:
        sig_b64 = data["signatureBase64"]

    payload = canonical_serialize_manifest(data)
    print(f"Canonical Payload ({len(payload)} bytes):")
    print(payload.decode("utf-8"))
    print("-" * 60)

    if sig_b64:
        ok = verify_signature(payload, sig_b64)
        print(f"Verification against 'learnmate_official_2026': {'VALID (PASS)' if ok else 'INVALID (FAIL)'}")
        sys.exit(0 if ok else 1)
    else:
        print("No signature provided to verify.")

if __name__ == "__main__":
    main()

