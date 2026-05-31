# Substrate Attestation Specification v0.1

**Status:** Draft
**Authors:** Andy Salvo (Crest Deployment Systems LLC)
**Origin:** A2A Discussion #1734 (CTEF RFC), Issue #1672 (Agent Identity Verification)
**First production binding:** commit [74764f2](https://github.com/aeoess/agent-governance-vocabulary/commit/74764f2) (2026-05-27)

---

## 1. Purpose

A `substrate_attestation` is a three-field structure that binds a verifier-issued receipt to a subject artifact. It carries enough information for any consumer to locate the receipt, verify its integrity, and identify who produced it, without embedding the verification logic or policy in the attestation itself.

The attestation answers three questions:
1. **Where is the receipt?** (`url`)
2. **What exact content was verified?** (`content_hash`)
3. **Who verified it?** (`verifier`)

It does NOT answer:
- Whether the receipt is correct
- Whether the verifier is trustworthy
- Whether the subject artifact is safe, compliant, or valuable
- What methodology the verifier used

Those judgments belong to the consumer, not the attestation.

---

## 2. Shape

```json
{
  "substrate_attestation": {
    "url": "<receipt-url>",
    "content_hash": "<hash-algorithm>:<hex-digest>",
    "verifier": "<did>"
  }
}
```

### 2.1 Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string (URL) | Yes | HTTPS URL where the full verification receipt can be dereferenced. MUST return `application/json`. MUST be stable (content at this URL MUST NOT change after publication; corrections are new URLs). |
| `content_hash` | string | Yes | Hash of the receipt body, formatted as `<algorithm>:<lowercase-hex-digest>`. The algorithm MUST be `sha256`. The digest MUST match `SHA-256(receipt_body_bytes)` where `receipt_body_bytes` is the raw bytes returned by dereferencing `url`. |
| `verifier` | string (DID) | Yes | A Decentralized Identifier (DID) that identifies the entity that produced the receipt. The DID method is not constrained: `did:web`, `did:key`, `did:aip`, or any W3C-conformant DID method is valid. The DID MUST resolve to a DID Document containing at least one verification method. |

### 2.2 Constraints

1. **Immutability.** Once published, the content at `url` MUST NOT change. If the verifier issues a correction, it MUST publish a new receipt at a new URL with a new `content_hash`. The original receipt remains accessible.

2. **Hash verification.** A consumer MUST be able to verify the attestation by: (a) fetching `url`, (b) computing `SHA-256(response_body)`, (c) comparing the result to `content_hash`. If they do not match, the attestation is invalid.

3. **Method agnosticism.** The `verifier` field accepts any valid DID. Consumers MUST NOT reject an attestation solely because the DID method is unfamiliar. Consumers MAY choose not to trust a particular verifier, but that is a policy decision, not a format violation.

4. **No schema absorption.** The attestation carries no per-implementation policy, no scoring thresholds, no enforcement rules. It is a pointer to evidence, not a judgment.

---

## 3. Verification Procedure

A consumer verifying a `substrate_attestation` performs these steps:

1. **Parse.** Extract `url`, `content_hash`, and `verifier` from the attestation object.

2. **Dereference.** Fetch `url` via HTTPS GET. The response MUST be `application/json`.

3. **Hash check.** Compute `SHA-256` of the raw response body. Compare to `content_hash` (stripping the `sha256:` prefix). If mismatch: INVALID.

4. **DID resolution (optional).** Resolve `verifier` to a DID Document. Verify that the DID Document contains a verification method. This step is OPTIONAL for format validation but RECOMMENDED for trust evaluation.

5. **Receipt inspection (consumer-defined).** The consumer reads the receipt JSON to determine the verification result (PASS, FAIL, PENDING, etc.). The attestation format imposes no constraints on receipt schema.

---

## 4. Relationship to CTEF

The `substrate_attestation` shape is designed to compose with the Composable Trust Evidence Format (CTEF). When included in a CTEF artifact:

- It occupies a defined field position alongside identity claims, behavioral evidence, and other trust signals.
- It does NOT replace or compete with other evidence types.
- It provides a content-addressed pointer to external verification evidence that CTEF gateways can dereference and factor into verdict computation.

### 4.1 Proposed CTEF normative language

> A CTEF artifact MAY include a `substrate_attestation` field. When present, the field MUST conform to the Substrate Attestation Specification. Consumers MUST preserve the field when forwarding artifacts and MUST report validation status (valid, invalid, or not checked) when processing it. Consumers MUST NOT infer substrate truth merely from field existence.

---

## 5. Examples

### 5.1 Valid attestation

```json
{
  "substrate_attestation": {
    "url": "https://verify.crestsystems.ai/agent-os-substrate-v1.json",
    "content_hash": "sha256:7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b",
    "verifier": "did:web:verify.crestsystems.ai"
  }
}
```

### 5.2 Valid attestation with did:aip verifier

```json
{
  "substrate_attestation": {
    "url": "https://example.com/receipts/abc123.json",
    "content_hash": "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    "verifier": "did:aip:devnet:7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU"
  }
}
```

### 5.3 Invalid attestation (hash mismatch)

```json
{
  "substrate_attestation": {
    "url": "https://verify.example.com/receipt.json",
    "content_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
    "verifier": "did:web:verify.example.com"
  }
}
```

If `SHA-256(fetch(url))` does not equal the stated hash, the attestation is INVALID regardless of receipt content.

---

## 6. Threat Model

| Threat | Mitigation |
|--------|-----------|
| Verifier lies about receipt content | Consumer verifies `content_hash` against fetched receipt |
| Receipt URL goes offline | Consumer caches receipt; `content_hash` proves the cached copy is authentic |
| Verifier DID is compromised | Consumer resolves DID and checks key material; revoked DIDs produce resolution failure |
| Attestation replayed from one artifact to another | `content_hash` binds to specific receipt content; receipts should include subject identifiers |
| Consumer treats field existence as endorsement | Spec explicitly states: field existence proves a receipt was issued, not that the subject is trustworthy |

---

## 7. What This Spec Does NOT Define

- **Receipt schema.** The JSON structure of the receipt itself is verifier-defined. This spec only requires that it be JSON and that its hash matches `content_hash`.
- **Verifier trust policy.** Whether a given verifier is trustworthy is a consumer decision. This spec provides the pointer; the consumer provides the judgment.
- **Scoring or thresholds.** No numeric scores, pass/fail thresholds, or enforcement rules are part of this spec.
- **Identity verification.** The `verifier` DID identifies the verifier but does not prove the verifier's competence or independence.

---

## 8. Conformance

An implementation conforms to this spec if:

1. It produces `substrate_attestation` objects with all three required fields.
2. The `url` field returns valid JSON via HTTPS GET.
3. The `content_hash` field matches `sha256:<lowercase-hex SHA-256 of url response body>`.
4. The `verifier` field is a syntactically valid DID.
5. Published attestations are immutable (corrections via new attestation, not mutation).

A conformance test suite is provided in `fixtures/` and can be run with `validate.py`.

---

## 9. Provenance

- **First specified:** A2A Discussion #1734, comment by @aeoess (2026-05-27)
- **First production binding:** commit [74764f2](https://github.com/aeoess/agent-governance-vocabulary/commit/74764f2), Matrix v1.1 Registry
- **First receipts produced:** verify.crestsystems.ai (7 receipts, Agent OS + argentum-core + CTEF + AURA + AP2)
- **First adoption:** Liuyanfeng1234 (Agent OS) adopted receipt as official substrate-attestation pointer (2026-05-28)
