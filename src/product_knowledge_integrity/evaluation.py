from __future__ import annotations

from typing import Any


def evaluate_answers(expected: list[dict[str, Any]], observed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected_by_id = {item["question_id"]: item for item in expected}
    results = []
    for answer in observed:
        checks = []
        for attribute_id, wanted in expected_by_id[answer["question_id"]]["expected_claims"].items():
            actual = answer["extracted_claims"].get(attribute_id)
            value = actual.get("value") if actual else None
            checks.append({"attribute_id": attribute_id, "expected": wanted["value"], "observed": value, "matches": value == wanted["value"]})
        results.append({"question_id": answer["question_id"], "language": answer["language"], "claim_checks": checks,
                        "accuracy_pass": all(item["matches"] for item in checks), "sources_used": answer.get("sources_used", [])})
    return results


def summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(result["accuracy_pass"] for result in results)
    return {"questions": len(results), "accuracy_passed": passed, "accuracy_rate_pct": round(100 * passed / len(results), 1) if results else 0.0}
