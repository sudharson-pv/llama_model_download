#!/usr/bin/env python3
"""
publish_release.py — Creates a GitHub Release on sudharson-pv/llama_model_download
and uploads model binaries, tokenizers, manifests, and signatures as release assets.
Retrieves auth token from git credential helper (never hardcoded).
"""
import argparse
import json
import mimetypes
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO_OWNER = "sudharson-pv"
REPO_NAME = "llama_model_download"

def get_github_token() -> str:
    """Retrieve GitHub token dynamically from Git Credential Manager."""
    try:
        proc = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n",
            capture_output=True,
            text=True,
            check=True
        )
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1]
    except Exception as e:
        print(f"Error retrieving credentials from git credential helper: {e}")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    raise RuntimeError("No GitHub token found in git credential helper or environment.")

def create_release(tag: str, name: str, body: str, token: str) -> dict:
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "LearnMate-Release-Manager",
        "Accept": "application/vnd.github+json"
    }

    # Check if release already exists
    req_check = urllib.request.Request(f"{url}/tags/{tag}", headers=headers)
    try:
        with urllib.request.urlopen(req_check) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"Release for tag '{tag}' already exists (ID: {data['id']}). Reusing.")
            return data
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise

    # Create new release
    payload = {
        "tag_name": tag,
        "target_commitish": "main",
        "name": name,
        "body": body,
        "draft": False,
        "prerelease": False
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"Successfully created release '{tag}' (ID: {data['id']}).")
        return data

def upload_asset(release: dict, file_path: Path, token: str):
    filename = file_path.name
    filesize = file_path.stat().st_size
    print(f"Uploading asset: {filename} ({filesize:,} bytes)...")

    # Check existing assets on release
    for asset in release.get("assets", []):
        if asset["name"] == filename:
            print(f"Asset '{filename}' already exists on release. Skipping.")
            return asset

    upload_url_template = release["upload_url"] # https://uploads.github.com/.../assets{?name,label}
    base_upload_url = upload_url_template.split("{")[0]
    upload_url = f"{base_upload_url}?name={urllib.parse.quote(filename)}"

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "LearnMate-Release-Manager",
        "Content-Type": "application/octet-stream",
        "Content-Length": str(filesize)
    }

    with open(file_path, "rb") as f:
        req = urllib.request.Request(upload_url, data=f, headers=headers, method="POST")
        with urllib.request.urlopen(req) as resp:
            asset_data = json.loads(resp.read().decode("utf-8"))
            print(f"Uploaded '{filename}' successfully -> {asset_data['browser_download_url']}")
            return asset_data

def main():
    parser = argparse.ArgumentParser(description="Publish model release to GitHub")
    parser.add_argument("--tag", required=True, help="Release tag (e.g. llama-3.2-1b-v1)")
    parser.add_argument("--name", required=True, help="Release name")
    parser.add_argument("--body", default="LearnMate AI official model release.", help="Release notes")
    parser.add_argument("--files", nargs="+", required=True, help="Files to upload as release assets")
    args = parser.parse_args()

    token = get_github_token()
    release = create_release(args.tag, args.name, args.body, token)

    for f in args.files:
        p = Path(f)
        if not p.is_file():
            print(f"Error: File not found: {p}")
            sys.exit(1)
        upload_asset(release, p, token)

    print("All release assets processed successfully.")

if __name__ == "__main__":
    main()

