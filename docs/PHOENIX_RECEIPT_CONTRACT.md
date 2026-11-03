# Phoenix Receipt Contract

The independent verifier checks a Phoenix proof-cycle export against its own declared schema, event lifecycle, timestamp order, SHA-256 event chain, finding commitment, terminal status, and evidence-boundary flags.

## Run locally

    python tools/phoenix_proof_cycle.py --self-test
    python tools/phoenix_proof_cycle.py --task "clean contract cycle" --output receipt.json
    python tools/phoenix_receipt_contract.py receipt.json
    python tools/test_phoenix_receipt_contract.py

To produce and verify a repaired receipt:

    python tools/phoenix_proof_cycle.py --task "seeded fault" --inject-defect --output repaired.json
    python tools/phoenix_receipt_contract.py repaired.json

## CI contract

The Phoenix Proof Cycle workflow runs the production runner's self-tests, the independent contract suite, and independent receipt checks for clean, repaired, and unrepaired-failure outcomes. It uploads all three receipts as workflow artifacts.

## Evidence boundary

The current Scout is a deterministic local fixture. These checks establish integrity and internal consistency of the supplied receipt, not external truth or independently anchored immutability. A SHA-256 chain can be recomputed by an actor who controls the data; independent anchoring must be claimed only after validating a real provider receipt.
