# substrate-attestation

[![CREST conformance](https://verify.crestsystems.ai/badge/cm-001.svg)](https://verify.crestsystems.ai/matrix)

A three-field shape for verifier-issued trust evidence in A2A agent ecosystems.

```json
{
  "substrate_attestation": {
    "url": "https://verify.example.com/receipt.json",
    "content_hash": "sha256:...",
    "verifier": "did:web:verify.example.com"
  }
}
```

Three fields. No schema absorption. Method-agnostic.

## What it does

Binds a verifier-issued receipt to a subject artifact. Any consumer can locate the receipt (`url`), verify its integrity (`content_hash`), and identify who produced it (`verifier`).

## What it does NOT do

- Prove the receipt is correct
- Assert the verifier is trustworthy
- Define receipt schema
- Impose scoring or enforcement policy

Those judgments belong to the consumer, not the attestation.

## Spec

[SPEC.md](SPEC.md) defines the field shapes, validation rules, verification procedure, threat model, and proposed CTEF normative language.

## Conformance

```bash
python3 validate.py
```

24 fixtures across format, verdict-binding, and key-rotation categories. The validator checks: field presence, hash format, DID syntax, URL scheme. Optional `--verify-hash` flag fetches the URL and verifies the content hash.

```bash
python3 validate.py --check '{"substrate_attestation": {"url": "https://...", "content_hash": "sha256:...", "verifier": "did:web:..."}}'
```

## Compatibility Matrix

[matrix.json](matrix.json) tracks who has been verified against what. 8 entries across 7 projects.

## Contributing Fixtures

See [FIXTURE_SCHEMA.md](FIXTURE_SCHEMA.md) for the canonical fixture format. Third-party fixtures go in `fixtures/contrib/`. PRs welcome.

## Origin

- Proposed by [@aeoess](https://github.com/aeoess) in [A2A #1672](https://github.com/a2aproject/A2A/issues/1672) and [Discussion #1734](https://github.com/a2aproject/A2A/discussions/1734)
- First production binding: [commit 74764f2](https://github.com/aeoess/agent-governance-vocabulary/commit/74764f2) in Matrix v1.1 Registry
- Receipts produced by [Crest Deployment Systems LLC](https://crestsystems.ai) at [verify.crestsystems.ai](https://verify.crestsystems.ai)

## License

Apache 2.0
