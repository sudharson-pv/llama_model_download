# Model Release Process

This document details how model releases are prepared, signed, and published to GitHub Releases for distribution to the LearnMate AI mobile application.

## Release Steps
1. **Model Qualification:** Ensure `.pte` and `tokenizer.model` pass native inference on physical test hardware (Motorola Moto G54 5G).
2. **Checksum Verification:** Run `python scripts/calculate_hashes.py <pte_file> <tokenizer_file>`.
3. **Manifest Creation:** Fill in `manifests/<model_id>.json`.
4. **Manifest Signing:** Execute `python scripts/sign_manifest.py manifests/<model_id>.json <private_key.pem>`.
5. **Catalog Update:** Update `catalog/catalog.json` and sign with `python scripts/sign_catalog.py catalog/catalog.json <private_key.pem>`.
6. **Publishing Release:** Run `scripts/publish_release.ps1 -Tag <tag> -Artifacts <files...>`.
7. **In-App Verification:** Confirm that the LearnMate AI application retrieves the catalog and downloads the release assets successfully.
