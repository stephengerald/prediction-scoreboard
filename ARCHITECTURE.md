# Architecture

## State machine

The owner creates a round, players submit confidence forecasts, the owner locks it and stores resolution evidence, consensus resolves it, and players claim deterministic scores.

The relevant roles are league owner and forecasters. Write methods enforce role, phase, uniqueness, and bounded-storage rules before any state transition.

## Consensus boundary

Validators interpret a stored resolution record under fixed league rules and return A, B, or UNRESOLVED; scoring itself is deterministic. The leader returns a small JSON schema; validators independently rerun the same decision function and accept only exact enum or bitmask values. Malformed model output raises a tagged model error and writes no decision.

## Deterministic boundary

Enrollment, authorization, commitments, counters, phase changes, caps, masks, and any score or credit arithmetic are deterministic contract logic. Only semantic interpretation of the stored evidence occurs inside `run_nondet_unsafe`.

## Off-chain boundary

Wallet custody, identity verification, indexing, notifications, private file storage, source authentication, money movement, legal process, and user-interface behavior are outside this repository. The organizer can submit misleading evidence. This is a non-custodial reputation game; money markets need independent sources, appeals, deadlines, and audited settlement.
