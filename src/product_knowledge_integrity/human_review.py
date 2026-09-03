from __future__ import annotations

from typing import Any


def record_decision(task: dict[str, Any], decision: str, reviewer_role: str, comment: str, proposed_correction: str | None = None) -> dict[str, Any]:
    if decision not in {"APPROVED", "CORRECTION_REQUIRED", "REJECTED"}:
        raise ValueError("unsupported review decision")
    return {"review_task_id": task["review_task_id"], "reviewer_role": reviewer_role, "decision": decision,
            "comment": comment, "affected_claim_ids": task["affected_claim_ids"], "proposed_correction": proposed_correction,
            "resulting_status": decision}


def corrected_variant(faulty_variant: dict[str, Any], corrected_claims: dict[str, Any], version: str) -> dict[str, Any]:
    result = {**faulty_variant, "version": version, "publication_status": "candidate", "derived_from": faulty_variant["version"], "claims": {**faulty_variant["claims"]}}
    result["claims"].update(corrected_claims)
    return result


def publication_status(qa_findings: list[dict[str, Any]]) -> str:
    return "APPROVED_FOR_PUBLICATION" if not any(item["severity"] == "critical" for item in qa_findings) else "NOT_APPROVED"
