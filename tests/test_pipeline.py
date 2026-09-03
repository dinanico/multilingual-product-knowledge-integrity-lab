from pathlib import Path

from product_knowledge_integrity.pipeline import run_pipeline

DATASET = Path(__file__).resolve().parents[1] / "examples/nexavolt_psx_24010"


def test_baseline_detects_source_drift_and_routes_review():
    report = run_pipeline(DATASET, "baseline")
    assert report["publication_gate"]["pass"] is False
    assert report["human_review_queue"][0]["status"] == "PENDING_REVIEW"
    assert report["ai_evaluation"]["summary"]["accuracy_rate_pct"] == 50.0
    assert report["root_causes"][0]["root_cause"] == "PUBLISHED_VARIANT_DRIFT"


def test_retest_closes_the_source_integrity_loop():
    report = run_pipeline(DATASET, "retest")
    assert report["publication_gate"]["pass"] is True
    assert report["ai_evaluation"]["summary"]["accuracy_rate_pct"] == 100.0
    assert report["root_causes"] == []
