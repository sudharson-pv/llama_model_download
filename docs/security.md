# Security & Cryptographic Integrity Guide

LearnMate AI employs an Ed25519 digital signature scheme and strict SHA-256 integrity verification to safeguard model distribution.

## Security Principles
1. **Zero Credential Commits:** Private keys, GitHub PATs, and sensitive tokens are strictly prohibited from Git history.
2. **Signature Enforcement:** Every manifest is verified against the publisher public key (`learnmate_official_2026`) embedded inside the Android APK.
3. **Quarantine Before Activation:** Downloaded assets are streamed into `.part` quarantine files. Atomic promotion to `.pte` occurs only after exact SHA-256 hash matching.
4. **Transport Security:** All downloads occur over TLS 1.3/HTTPS. Cleartext (HTTP) traffic is prohibited in the Android manifest and network security configuration.
