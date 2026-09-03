from __future__ import annotations

from typing import Any


def identify_claims(product_truth: dict[str, Any]) -> list[dict[str, Any]]:
    """Turn structured Product Truth attributes into stable product claims."""
    return [{"claim_id": f"claim:{attribute_id}", "product_id": product_truth["product_id"],
             "attribute_id": attribute_id, "canonical_value": spec["value"], "unit": spec.get("unit"),
             "criticality": spec.get("criticality", "medium"), "concept_id": spec.get("concept_id"),
             "source_ref": product_truth["source_ref"], "source_version": product_truth["version"]}
            for attribute_id, spec in product_truth["attributes"].items()]
