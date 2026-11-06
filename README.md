# LearnMate AI — Model Distribution Infrastructure

Official model distribution repository for **LearnMate AI** (`com.learnmate.ai`), hosting verified on-device Meta Llama models compiled for Meta's ExecuTorch runtime with CPU/XNNPACK acceleration.

---

## 📂 Repository Structure

```
llama_model_download/
├── README.md
├── catalog/
│   ├── catalog.json              # Signed multi-model catalog index
│   └── catalog.sig               # Ed25519 signature of catalog.json
├── manifests/
│   ├── llama-3.2-1b.json         # Manifest for Llama 3.2 1B Instruct
│   ├── llama-3.2-1b.sig          # Ed25519 signature for 1B manifest
│   ├── llama-3.2-3b.json         # Manifest for Llama 3.2 3B Instruct
│   └── llama-3.2-3b.sig          # Ed25519 signature for 3B manifest
├── metadata/
│   ├── versions.json             # Distribution version tracking
│   └── compatibility.json        # Hardware tier and RAM gating rules
├── scripts/
│   ├── calculate_hashes.py       # Computes SHA-256 and byte sizes
│   ├── validate_manifest.py      # Verifies manifest canonical payloads
│   ├── sign_manifest.py          # Signs manifests using Ed25519
│   ├── sign_catalog.py           # Signs catalog using Ed25519
│   ├── publish_release.py        # Creates GitHub Releases and uploads assets
│   └── publish_release.ps1       # PowerShell wrapper for release publication
└── docs/
    ├── model_setup.md            # Model export and compilation guide
    ├── release_process.md        # Step-by-step release workflow
    └── security.md               # Cryptographic integrity and key safety
```

---

## 🛡️ Model Verification & Cryptographic Provenance

All model manifests and catalogs in this repository are cryptographically signed using **Ed25519** with publisher key `learnmate_official_2026`:

- **Publisher Public Key (X.509 DER, Base64):**
  ```
  MCowBQYDK2VwAyEAN77dwAlm5tC1Nzatm0F/6jbLXvdXmDZw8tXbsNaWl+A=
  ```
- **Quarantine and Atomic Promotion:**
  LearnMate AI downloads models into temporary `.part` quarantine files. The application validates the SHA-256 checksum and manifest signature before promoting the model to internal storage.
- **Fail-Closed Execution:**
  GGUF models, truncated binaries, tampered manifests, or unverified signatures are strictly rejected.

---

## 🚀 Active Releases

| Release Tag | Model Name | Format | Size | SHA-256 |
|---|---|---|---|---|
| [`llama-3.2-1b-v1`](https://github.com/sudharson-pv/llama_model_download/releases/tag/llama-3.2-1b-v1) | Meta Llama 3.2 1B Instruct | ExecuTorch PTE | 803,033,472 B | `aa1e127484fed5bb2b28ba7f774fcd206c1f2f997ed71cfd9ded800956eb5301` |
| [`llama-3.2-1b-v1`](https://github.com/sudharson-pv/llama_model_download/releases/tag/llama-3.2-1b-v1) | Tokenizer | TikToken / BPE | 2,183,982 B | `82e9d31979e92ab929cd544440f129d9ecd797b69e327f80f17e1c50d5551b55` |

---

## 📜 Licensing & Attribution
Models distributed in this repository are built with Meta Llama 3.2 and Meta Llama 3.1 and subject to the **Meta Llama Community License Agreement**. Copyright (c) Meta Platforms, Inc. All rights reserved.
