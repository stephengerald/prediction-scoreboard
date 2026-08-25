# Submission: Prediction Scoreboard

Project name: Prediction Scoreboard

Repository: https://github.com/stephengerald/prediction-scoreboard

StudioNet contract: https://explorer-studio.genlayer.com/address/0xAE8Bf80C42c6282410CcEB01a5Db50b71AFa4663

Deployment transaction: https://explorer-studio.genlayer.com/tx/0x83aff0d57f4cfbd22c8b1781372df00e917b451a7eb2f7fe8578d007894b57e4

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x445ced3d41e4101dfb2003069d553a5a3347e0a97fcc7cc59939d52be1e2ea45

Summary: Runs reusable two-option forecasting rounds and computes deterministic integer Brier-style scores after consensus resolution.

Why it is GenLayer-native: Validators interpret a stored resolution record under fixed league rules and return A, B, or UNRESOLVED; scoring itself is deterministic.

Evidence/source model: Resolution uses only the owner's stored evidence and constructor-fixed rules. No external source is fetched or authenticated by this version.

Declared scope: Reusable, non-custodial prototype. The organizer can submit misleading evidence. This is a non-custodial reputation game; money markets need independent sources, appeals, deadlines, and audited settlement.

Review evidence: `AUDIT.md`, `SECURITY.md`, `SOURCE_POLICY.md`, and `deployments/studionet.json` bind the reviewed source hash to the public live result.
