# Prediction Scoreboard

Runs reusable two-option forecasting rounds and computes deterministic integer Brier-style scores after consensus resolution.

## Why GenLayer

Validators interpret a stored resolution record under fixed league rules and return A, B, or UNRESOLVED; scoring itself is deterministic.

## Reusable workflow

The owner creates a round, players submit confidence forecasts, the owner locks it and stores resolution evidence, consensus resolves it, and players claim deterministic scores. Constructor parameters create a new independent instance, so the code is reusable; state is not shared between deployments.

The contract is deliberately non-custodial. It records a decision, entitlement, score, or approval signal and never transfers GEN.

## Evidence boundary

Resolution uses only the owner's stored evidence and constructor-fixed rules. No external source is fetched or authenticated by this version.

## Verify locally

```powershell
genvm-lint check contracts/prediction_scoreboard.py
genvm-lint typecheck contracts/prediction_scoreboard.py
pytest tests/direct -q
python tests/run_glsim.py --validators 5
```

With GLSim running in another terminal:

```powershell
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The live smoke test requires fresh test-only keys in `GENLAYER_PRIVATE_KEY`, `GENLAYER_SECONDARY_PRIVATE_KEY`. Never commit a `.env` file or use a production wallet.

```powershell
gltest tests/integration/test_studionet_smoke.py --network studionet -s -q --default-wait-interval=6000 --default-wait-retries=240
```

Use the documented 6-second StudioNet polling interval to stay comfortably below public endpoint limits.

See `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md`, and `deployments/studionet.json` for the review boundary and exact public evidence.
