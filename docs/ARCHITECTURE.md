# Architecture

The integrity unit is a structured Product Claim, not a translation segment. The pipeline loads canonical Product Truth, normalizes multilingual variants into stable claims, runs deterministic QA, routes critical drift to review, evaluates observed AI answers, and diagnoses whether a wrong answer reproduced a wrong published source.

The package intentionally has no database, browser automation, TMS, CMS/PIM integration, background workers, or hosted UI.
