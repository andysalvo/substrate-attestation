# ambiguous_issuer_binding fixtures

Vectors testing cross-issuer attestation composition when issuers
are not genuinely independent. These fixtures should FAIL CLOSED
in any correct verifier.

## The problem

Two attestations can individually pass all format, hash, and
signature checks while composing into a false trust signal.
This happens when:

1. Both attestations share a common origin (same org, same
   infrastructure, same training data) despite having different
   DIDs
2. The `action_ref` is identical in both envelopes, so hash
   recomputation passes on both
3. A naive verifier treats two passing attestations as
   independent confirmation

The result: manufactured consensus from a single source.

## Why this matters

Cross-issuer composition only means something if the issuers are
genuinely independent. Non-independence is exactly the failure mode
these vectors test for.

Reference: aeoess on A2A Discussion #1734 (2026-06-02):
"Cross-issuer composition only means something if the two issuers
and the vector author are genuinely independent, because
non-independence is exactly the failure mode this problem tests for."

## Expected behavior

A correct verifier MUST:
- Detect shared-origin attestations before composing
- Reject composition when issuer independence cannot be verified
- Treat two attestations from the same infrastructure as ONE
  attestation, not two

A naive verifier will:
- Accept both attestations individually (they are format-valid)
- Compose them as independent confirmation
- Produce a false "multi-issuer verified" signal
