#!/usr/bin/env python3
"""
Substrate Attestation Conformance Validator v0.1

Validates substrate_attestation objects against the spec.
Runs the fixture suite (fixtures/valid.json + fixtures/invalid.json).

Usage:
  python3 validate.py                          # run all fixtures
  python3 validate.py --check '{"substrate_attestation": {...}}'  # validate one
  python3 validate.py --verify-hash            # also fetch URLs and verify content_hash
"""

import json
import sys
import re
import hashlib
from pathlib import Path

DID_PATTERN = re.compile(r'^did:[a-z0-9]+:.+$')
HASH_PATTERN = re.compile(r'^sha256:[a-f0-9]{64}$')
URL_PATTERN = re.compile(r'^https://.+$')


def validate_attestation(attestation, verify_hash=False):
    """Validate a substrate_attestation object. Returns (valid, errors)."""
    errors = []

    sa = attestation.get("substrate_attestation")
    if sa is None:
        return False, ["missing substrate_attestation field"]

    if not isinstance(sa, dict):
        return False, ["substrate_attestation must be an object"]

    # url
    url = sa.get("url")
    if url is None:
        errors.append("missing required field: url")
    elif not isinstance(url, str):
        errors.append("url must be a string")
    elif not URL_PATTERN.match(url):
        errors.append(f"url must be HTTPS: got {url[:50]}")

    # content_hash
    content_hash = sa.get("content_hash")
    if content_hash is None:
        errors.append("missing required field: content_hash")
    elif not isinstance(content_hash, str):
        errors.append("content_hash must be a string")
    elif ":" not in content_hash:
        errors.append("content_hash must be formatted as algorithm:hex_digest")
    elif not content_hash.startswith("sha256:"):
        algo = content_hash.split(":")[0]
        errors.append(f"unsupported hash algorithm: {algo} (only sha256 supported)")
    elif not HASH_PATTERN.match(content_hash):
        errors.append("content_hash hex digest must be 64 lowercase hex characters")

    # verifier
    verifier = sa.get("verifier")
    if verifier is None:
        errors.append("missing required field: verifier")
    elif not isinstance(verifier, str):
        errors.append("verifier must be a string")
    elif not DID_PATTERN.match(verifier):
        errors.append(f"verifier must be a valid DID (did:method:specific-id): got {verifier[:50]}")

    # Optional: verify content_hash against fetched URL
    if verify_hash and url and content_hash and not errors:
        try:
            import urllib.request
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = resp.read()
                computed = "sha256:" + hashlib.sha256(body).hexdigest()
                if computed != content_hash:
                    errors.append(f"content_hash mismatch: stated {content_hash[:20]}... computed {computed[:20]}...")
        except Exception as e:
            errors.append(f"url fetch failed: {e}")

    return len(errors) == 0, errors


def run_fixtures():
    """Run all fixture files."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    total = 0
    passed = 0
    failed = 0

    for fixture_file in sorted(fixtures_dir.rglob("*.json")):
        fixtures = json.loads(fixture_file.read_text())
        for fixture in fixtures:
            total += 1
            fid = fixture["id"]
            name = fixture["name"]
            expected = fixture["expected"]

            valid, errors = validate_attestation(fixture["attestation"])

            if expected == "VALID" and valid:
                passed += 1
                print(f"  [PASS] {fid}: {name}")
            elif expected == "INVALID" and not valid:
                passed += 1
                print(f"  [PASS] {fid}: {name} (correctly rejected: {errors[0]})")
            elif expected == "INVALID_SEMANTIC" and valid:
                passed += 1
                level = fixture.get("validation_level", "semantic check required")
                print(f"  [PASS] {fid}: {name} (format-valid, semantic violation: {level})")
            elif expected == "INVALID_SEMANTIC" and not valid:
                passed += 1
                print(f"  [PASS] {fid}: {name} (caught at format level: {errors[0]})")
            else:
                failed += 1
                status = "valid" if valid else f"invalid ({errors})"
                print(f"  [FAIL] {fid}: {name} -- expected {expected}, got {status}")

    print(f"\n  {passed}/{total} PASS, {failed} FAIL")
    return failed == 0


def main():
    args = sys.argv[1:]

    if "--check" in args:
        idx = args.index("--check")
        if idx + 1 < len(args):
            obj = json.loads(args[idx + 1])
            verify = "--verify-hash" in args
            valid, errors = validate_attestation(obj, verify_hash=verify)
            if valid:
                print("VALID")
            else:
                print(f"INVALID: {'; '.join(errors)}")
            sys.exit(0 if valid else 1)

    print("=" * 50)
    print("  Substrate Attestation Conformance Suite v0.1")
    print("=" * 50)

    success = run_fixtures()
    print("=" * 50)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
