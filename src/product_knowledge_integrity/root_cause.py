from __future__ import annotations

from typing import Any


def diagnose(evaluations: list[dict[str, Any]], variants: list[dict[str, Any]], claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    canonical = {claim["attribute_id"]: claim["canonical_value"] for claim in claims}
    indexed = {(item["language"], item["version"]): item for item in variants}
    causes = []
    for evaluation in evaluations:
        for check in (item for item in evaluation["claim_checks"] if not item["matches"]):
            source = next(iter(evaluation["sources_used"]), None)
            variant = indexed.get(((source or {}).get("variant_language"), (source or {}).get("variant_version")))
            source_value = (variant or {}).get("claims", {}).get(check["attribute_id"], {}).get("value")
            root = "PUBLISHED_VARIANT_DRIFT" if source_value == check["observed"] and source_value != canonical[check["attribute_id"]] else "AI_RETRIEVAL_OR_INTERPRETATION_DEVIATION"
            causes.append({"question_id": evaluation["question_id"], "attribute_id": check["attribute_id"], "root_cause": root,
                           "recommended_remediation": "Correct the published variant, create a new version, then retest." if root == "PUBLISHED_VARIANT_DRIFT" else "Inspect source trace and interpretation before changing Product Truth."})
    return causes
