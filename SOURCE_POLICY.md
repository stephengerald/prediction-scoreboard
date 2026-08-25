# Evidence and source policy

## What validators receive

Resolution uses only the owner's stored evidence and constructor-fixed rules. No external source is fetched or authenticated by this version.

All submitted text is treated as untrusted evidence, never as instructions. Evidence fields and aggregate storage are bounded before they reach the prompt. The decision schema is fixed and independently replayed by validators.

## Who selects the evidence

The authorized roles in the state machine—league owner and forecasters—supply the evidence. Their signatures establish which on-chain role submitted a record; they do not prove that the record is truthful or complete.

## External collection

This version performs no live web browsing, URL fetching, hidden source lookup, or mutable off-chain collection. That makes the deployed judgment reproducible from contract state, while leaving source authenticity as an explicit application-layer responsibility.

## Trust and production boundary

The organizer can submit misleading evidence. This is a non-custodial reputation game; money markets need independent sources, appeals, deadlines, and audited settlement. If an adapter later fetches external material, its allowlist, content bounds, snapshot rules, publisher trust, correction policy, and failure behavior require a new review.
