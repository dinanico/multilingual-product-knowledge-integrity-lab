from product_knowledge_integrity.human_review import corrected_variant, publication_status, record_decision


def test_decision_and_new_version_preserve_history():
    task = {"review_task_id": "review:it:input_phase_count:1.0.0", "affected_claim_ids": ["input_phase_count"]}
    decision = record_decision(task, "CORRECTION_REQUIRED", "language_specialist", "Three phases conflict with Product Truth.", "Use monofase.")
    faulty = {"version": "1.0.0", "publication_status": "published", "claims": {"input_phase_count": {"value": 3}}}
    corrected = corrected_variant(faulty, {"input_phase_count": {"value": 1}}, "1.0.1")
    assert decision["resulting_status"] == "CORRECTION_REQUIRED"
    assert faulty["claims"]["input_phase_count"]["value"] == 3
    assert corrected["derived_from"] == "1.0.0" and corrected["claims"]["input_phase_count"]["value"] == 1
    assert publication_status([]) == "APPROVED_FOR_PUBLICATION"
