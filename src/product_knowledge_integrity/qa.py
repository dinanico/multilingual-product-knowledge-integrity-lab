from __future__ import annotations

from typing import Any


def _same(left: Any, right: Any) -> bool:
    return left.strip().casefold() == right.strip().casefold() if isinstance(left, str) and isinstance(right, str) else left == right


def normalize_variant(variant: dict[str, Any], claims: list[dict[str, Any]]) -> dict[str, Any]:
    canonical = {claim["attribute_id"]: claim for claim in claims}
    return {"variant_id": variant["variant_id"], "language": variant["language"], "version": variant["version"],
            "publication_status": variant["publication_status"], "claims": {
                attribute_id: {"attribute_id": attribute_id, "claim_id": canonical[attribute_id]["claim_id"],
                               "value": value["value"], "unit": value.get("unit"), "surface_form": value.get("surface", ""),
                               "concept_id": value.get("concept_id")} for attribute_id, value in variant["claims"].items()}}


def run_qa(claims: list[dict[str, Any]], variants: list[dict[str, Any]]) -> list[dict[str, Any]]:
    canonical = {claim["attribute_id"]: claim for claim in claims}
    findings: list[dict[str, Any]] = []
    for variant in variants:
        for attribute_id, claim in canonical.items():
            observed = variant["claims"].get(attribute_id)
            if observed is None:
                findings.append({"type": "MISSING_CLAIM", "severity": "critical", "attribute_id": attribute_id, "claim_id": claim["claim_id"], "language": variant["language"], "variant_version": variant["version"]})
            elif not _same(observed["value"], claim["canonical_value"]) or not _same(observed.get("unit"), claim.get("unit")):
                findings.append({"type": "FACTUAL_DRIFT", "severity": "critical" if claim["criticality"] == "critical" else "warning", "attribute_id": attribute_id, "claim_id": claim["claim_id"], "language": variant["language"], "variant_version": variant["version"], "expected": claim["canonical_value"], "actual": observed["value"]})
    return findings


def route_human_review(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"review_task_id": f"review:{item['language']}:{item['attribute_id']}:{item['variant_version']}",
             "status": "PENDING_REVIEW", "mandatory": True, "triggered_by": item,
             "affected_claim_ids": [item["attribute_id"]]} for item in findings if item["severity"] == "critical"]
