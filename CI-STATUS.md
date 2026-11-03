# CI Status

No hosted CI workflow was added by this upgrade because the current GitHub credential cannot create or update workflow files. The local deterministic validation command remains available at `python3 scripts/splus_check.py`. No source content was deleted or overwritten.

## Hosted CI evidence reconciliation — observed 2026-11-03

The earlier note above records a historical limitation from a prior upgrade. The current default branch contains hosted Phoenix Audit and Phoenix Proof Cycle workflows.

- **Phoenix Audit on main:** run [#40144578951](https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE/actions/runs/40144578951) completed successfully for commit `146d533f6b6f394c7b522dde9e5b2c965e4b14f9`. The audit job reported success for Python, Node, Go, Rust, Java, credential-pattern scan, federation contract audit, and audit-manifest steps.
- **Phoenix Proof Cycle:** the latest returned successful run is [#38952339627](https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE/actions/runs/38952339627) on branch `phoenix/receipt-contract-2026-10-16`, commit `6395cb6a5409f2e280b2f2ef11de5cdd3f6cc110`. Its self-tests, independent receipt-contract tests, clean cycle, seeded-defect repair/re-verification, explicit unrepaired-failure check, and artifact upload all completed successfully.
- **Proof-cycle artifact:** `phoenix-proof-cycle-receipts`, artifact ID `12067868939`, SHA-256 digest `1234416a4098729b5f9a58241dcd9bb15963eee5f77c99b69456c29f24b0f366`, retained until 2027-01-14.

**Scope boundary:** the successful proof-cycle run is branch-specific, not a fresh run on the current `main` commit. The fixture validates deterministic local verification and receipt integrity; it does not establish external AI execution, live web research, Bitcoin/Arweave/OpenTimestamps anchoring, or production deployment.

## Fresh proof-cycle revalidation — 2026-11-03

- **Run:** [Phoenix Proof Cycle #41708062905](https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE/actions/runs/41708062905), successful on branch `automation/phoenix-crossconnect-ci-status-20261103-1140`, commit `408cfe4d66f377c53c4ee3327f0efeaa1c3d2b6f`.
- **Tests:** 8 deterministic runner self-tests and 13 independent receipt-contract tests passed. The clean, bounded-repair, and unrepaired-failure scenarios each produced a receipt accepted by the independent verifier. The unrepaired scenario returned the expected explicit exit code `2` and was not converted into success.
- **Artifact:** `phoenix-proof-cycle-receipts`, ID `13266960899`, 3,176 bytes, SHA-256 `87fae1f79ae4ed847dcd4da2665bce76dff08741bb9df9b615151e71f1227796`; retained until 2026-12-03.
- **Independent read-back:** the downloaded ZIP digest matched GitHub's artifact digest. All three receipts passed export-hash, finding-hash, event-chain, lifecycle, terminal-binding, and evidence-boundary checks. Direct finding tampering and finding tampering with a recomputed outer export hash were both rejected.
- **Receipt outcomes:** clean `PASS` (4 events); seeded defect with one bounded repair `REPAIRED` (6 events); seeded defect without repair `FAIL` (4 events). All five external-evidence flags (`external_ai`, `web_research`, `bitcoin_anchor`, `arweave_anchor`, `ots_anchor`) are `false` in every receipt.
- **Audit:** [Phoenix Audit #41708062877](https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE/actions/runs/41708062877) completed successfully, including Python, Node, Go, Rust, Java, credential-pattern, federation-contract, and audit-manifest steps.

**Scope boundary:** this is a fresh branch-specific CI fixture, not a run on current `main`. It establishes internal receipt integrity and explicit failure behavior; it does not establish external AI execution, real web research, external timestamp anchoring, production deployment, or live distributed federation.

### Latest proof-cycle-validated code head (before the evidence-only status append)

- **Proof Cycle:** [run #41708321444](https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE/actions/runs/41708321444) completed successfully on code head `52290b38c31297fab64db9a49d46b25c6ac2a773`. The branch later advanced to `3660dc971fab3a898b5536b8455fd1daf9e2496a` and then `625cfb3de12262cff67852fa05675040ee1301b8` for evidence-only status-note clarifications; the proof-cycle code and workflow were unchanged.
- **Artifact:** ID `13267390936`, 3,175 bytes, SHA-256 `3a5da033af7f9a8ad4528c51688e03e73300c8f5bccc1ef3191cadca9688824e`.
- **Independent read-back:** downloaded ZIP SHA-256 matches the GitHub digest; all three receipts independently verify as `PASS` (4 events), `REPAIRED` (6 events), and explicit `FAIL` (4 events). All five external-evidence flags remain false in each receipt.
- **Audit:** [Phoenix Audit #41708321215](https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE/actions/runs/41708321215) completed successfully on the same tested code head.

## 2026-11-03 — final receipt-contract hardening and post-merge verification

The independent receipt verifier now rejects external-evidence flags in the deterministic fixture, binds pre-repair errors to the initial verifier ledger event, and rejects boolean sequence values.

Final PR-head run [#41711762834](https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE/actions/runs/41711762834) passed:
- 8 Phoenix runner self-tests.
- 15 independent receipt-contract tests.
- PASS, REPAIRED, and FAIL receipt verification, with 4, 6, and 4 hash-chained events respectively.

Artifact ID: `13266249198`  
Artifact SHA-256: `60d43cee4cedce9dd28fa5513c21dbbfbfb6dab110536026f1bc84e2d9cbf1f3`

The artifact ZIP was downloaded and its SHA-256 independently recalculated. Each receipt's outer export hash, finding hash, ledger chain, terminal binding, and five false external-evidence flags were independently checked.

PR #4 merged as `4b91814f906ea7943625544958c88d9cb8f0aea7`. Post-merge [Proof Cycle #41711973409](https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE/actions/runs/41711973409) and [Phoenix Audit #41711973487](https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE/actions/runs/41711973487) both passed.

Federation-wide record: [2026-11-03 propagation and receipt-hardening evidence](https://github.com/Zygros/sovereign-federation/blob/main/evidence/audits/2026-11-03-federation-propagation-and-receipt-hardening.md).
