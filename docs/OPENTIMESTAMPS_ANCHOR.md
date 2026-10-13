# OpenTimestamps Anchor Procedure for Demonstration Zero

## Target

Final state hash: `281a9c6b944d30220be7b209492d2183d3931f94175d086b7cd90995cfe05593`

Permaweb anchor (existing): `eba44d95634073ea8e14960e52`

## Why Bitcoin

OpenTimestamps proves a file existed at a given time by embedding its hash commitment into the Bitcoin blockchain. No trusted third party. The Bitcoin block is the witness. Anyone can verify independently with the ots client.

## Steps

1. Save the final state hash as a plain text file:
   ```
   echo -n 281a9c6b944d30220be7b209492d2183d3931f94175d086b7cd90995cfe05593 > demo_zero_hash.txt
   ```
2. Create the timestamp:
   ```
   ots stamp demo_zero_hash.txt
   ```
   This produces `demo_zero_hash.txt.ots`.
3. Upgrade to Bitcoin (wait for a block, usually under an hour):
   ```
   ots upgrade demo_zero_hash.txt.ots
   ```
4. Verify:
   ```
   ots verify demo_zero_hash.txt.ots
   ```
   Expected: `Success! Bitcoin block <N> attests to existence of demo_zero_hash.txt`.
5. Commit `demo_zero_hash.txt` and `demo_zero_hash.txt.ots` to this repository.

## What the Anchor Proves

- The hash existed before the Bitcoin block timestamp.
- The recursion trace that produced it is reproducible from the public script.
- No central authority vouches; the chain does.

## What It Does Not Prove

- Intelligence.
- Correctness of the thesis.
- That 74,088,000 agents are running.

It proves provenance and ordering. That is the floor, not the ceiling.

Always add. Never take.
