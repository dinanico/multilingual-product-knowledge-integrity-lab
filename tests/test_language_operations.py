from product_knowledge_integrity.propagation import extract_claims


def test_phase_forms_normalize_across_languages_without_correcting_three_phase():
    for text in ("single-phase AC input", "einphasigem AC-Eingang", "ingresso AC monofase"):
        assert extract_claims(text)["input_phase_count"]["value"] == 1
    for text in ("three-phase AC input", "dreiphasiger AC-Eingang", "ingresso AC trifase"):
        assert extract_claims(text)["input_phase_count"]["value"] == 3


def test_din_rail_forms_map_to_one_concept_but_unknown_mounting_does_not():
    for text in ("DIN rail mounting", "DIN-Schienenmontage", "montaggio su guida DIN"):
        assert extract_claims(text)["mounting"]["normalized_concept"] == "DIN_RAIL"
    assert "mounting" not in extract_claims("wall-mounted enclosure")


def test_voltage_and_current_preserve_the_actual_numeric_value():
    assert extract_claims("24-V-DC output, 10 A")["output_voltage"]["value"] == 24
    assert extract_claims("48 V DC, 12A")["output_voltage"]["value"] == 48
    assert extract_claims("48 V DC, 12A")["nominal_output_current"]["value"] == 12
