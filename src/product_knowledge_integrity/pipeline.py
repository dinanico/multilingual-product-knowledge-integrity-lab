from __future__ import annotations

from pathlib import Path
from typing import Any

from .claims import identify_claims
from .evaluation import evaluate_answers, summary
from .io import load_json
from .qa import normalize_variant, route_human_review, run_qa
from .root_cause import diagnose


def run_pipeline(dataset_dir: str | Path, phase: str = "baseline") -> dict[str, Any]:
    """Run the deterministic NexaVolt source-integrity demonstration."""
    if phase not in {"baseline", "retest"}:
        raise ValueError("phase must be baseline or retest")
    dataset = Path(dataset_dir)
    truth = load_json(dataset / "product_truth.json")
    claims = identify_claims(truth)
    variants = [normalize_variant(item, claims) for item in load_json(dataset / f"multilingual_variants.{phase}.json")["variants"]]
    findings = run_qa(claims, variants)
    review_queue = route_human_review(findings)
    evaluations = evaluate_answers(load_json(dataset / "expected_answers.json")["answers"], load_json(dataset / f"observed_ai_answers.{phase}.json")["answers"])
    roots = diagnose(evaluations, variants, claims)
    return {"pipeline_version": "public-0.1.0", "phase": phase,
            "product": {"product_id": truth["product_id"], "product_name": truth["product_name"], "truth_version": truth["version"]},
            "product_claims": claims, "normalized_variants": variants, "qa_findings": findings,
            "human_review_queue": review_queue, "publication_gate": {"pass": not any(item["severity"] == "critical" for item in findings), "mandatory_human_reviews": len(review_queue)},
            "ai_evaluation": {"summary": summary(evaluations), "results": evaluations}, "root_causes": roots}
