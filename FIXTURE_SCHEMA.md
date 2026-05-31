# Canonical Fixture Schema v0.1

All fixtures in this repo and contributed fixtures follow this schema. Any conformance suite in the ecosystem can consume fixtures in this format without translation.

## Schema

```json
{
  "id": "string (unique, kebab-case, e.g. 'sa-valid-001' or 'kr-invalid-002')",
  "name": "string (human-readable, one line)",
  "description": "string (what this fixture tests and why it matters)",
  "category": "string (see categories below)",
  "expected": "VALID | INVALID | INVALID_SEMANTIC",
  "validation_level": "format | semantic | runtime (what level of validator catches this)",
  "attestation": {
    "substrate_attestation": {
      "url": "string",
      "content_hash": "string",
      "verifier": "string"
    }
  },
  "failure_mode": "string or null (machine-readable label when expected != VALID)",
  "note": "string or null (optional context for implementers)",
  "contributed_by": "string or null (GitHub handle or org, for attribution)",
  "spec_ref": "string or null (section of SPEC.md or external spec this exercises)"
}
```

## Categories

| Category | Description |
|---|---|
| `format` | Field presence, types, patterns (url, hash, DID syntax) |
| `verdict-binding` | content_hash binds to verdict record, not detected content |
| `key-rotation` | Rotated vs revoked keys, resolve-at-time semantics |
| `did-method` | Method-specific behavior (did:web, did:aip, did:key) |
| `lifecycle` | Freshness, expiry, revocation, status transitions |
| `disagreement` | Verdict reconciliation across verifiers |
| `refusal` | Declined actions as structured evidence |
| `near-miss` | Ambiguous issuer binding, rescoped replay, semantic drift |
| `adversarial` | Intentionally malicious or edge-case inputs |

## Expected values

- `VALID`: a conforming validator MUST accept this
- `INVALID`: a conforming validator MUST reject this (detectable at format level)
- `INVALID_SEMANTIC`: format-valid but semantically wrong (requires URL fetch, DID resolution, or receipt inspection to detect)

## Naming convention

`{category}-{valid|invalid}-{NNN}` where NNN is zero-padded.

Examples: `format-valid-001`, `kr-invalid-002`, `vb-invalid-003`, `nm-adversarial-001`

## Contributed fixtures

Third-party fixtures go in `fixtures/contrib/{github-handle}/`. Same schema. Attribution via `contributed_by` field. Reviewed before merge but not modified.

## Referencing external vectors

External vector corpora (e.g., CTEF test vectors, AlgoVoi JCS corpus) are referenced by URL + commit hash + retrieval hash. They are not copied into this repo. The reference is recorded in `matrix.json`.
