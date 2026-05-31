# Contributing Fixtures

Third-party conformance fixtures go here. Each contributor gets a directory named by their GitHub handle.

## How to contribute

1. Fork this repo
2. Create `fixtures/contrib/{your-github-handle}/`
3. Add fixtures following [FIXTURE_SCHEMA.md](../../FIXTURE_SCHEMA.md)
4. Run `python3 validate.py` to verify your fixtures parse correctly
5. Open a PR

## What we accept

- **Format fixtures**: test field presence, types, patterns
- **Semantic fixtures**: test behavior that requires URL fetch, DID resolution, or receipt inspection (mark as `INVALID_SEMANTIC`)
- **Method-specific fixtures**: test DID method behavior (did:aip resolve-at-time, did:web key rotation, etc.)
- **Near-miss fixtures**: ambiguous cases that exercise boundary conditions
- **Adversarial fixtures**: intentionally malicious inputs

## What we do with contributions

- Review for schema compliance (we do not modify your fixtures)
- Add to the compatibility matrix (`matrix.json`)
- Attribute via `contributed_by` field
- Run against our validator and publish results

## Currently expected contributions

| Contributor | Fixture Set | Status |
|---|---|---|
| dr-wilson-empty | did:aip live-reject + resolve-at-time-accept | Offered, awaiting PR |
| kenneives | CTEF near-miss vectors (referenced, not copied) | Referenced at agentgraph@a07cdf8 |
| chopmob-cloud | JCS cross-validation corpus (referenced, not copied) | Referenced at algovoi-jcs-conformance-vectors |
