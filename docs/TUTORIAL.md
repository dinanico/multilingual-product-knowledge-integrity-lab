# NexaVolt tutorial

NexaVolt Labs and PSX-24010 are fictional.

1. Inspect `examples/nexavolt_psx_24010/product_truth.json`: the canonical input phase count is one.
2. Run the deterministic baseline command from the README.
3. Inspect the Italian `1.0.0` variant: it says three phases.
4. Observe the critical QA finding and mandatory review item.
5. Observe the deterministic Italian AI answer reproducing the published three-phase value.
6. Inspect the root cause: `PUBLISHED_VARIANT_DRIFT`.
7. Inspect the Italian `1.0.1` retest variant, derived from `1.0.0` and corrected to one phase.
8. Run the retest; QA and AI evaluation pass.

The files under `reports/examples/` summarize this story as curated deterministic examples. Optional OpenAI use is separate and never required for this tutorial.
