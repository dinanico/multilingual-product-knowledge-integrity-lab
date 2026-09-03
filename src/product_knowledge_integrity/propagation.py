from __future__ import annotations

import re
from typing import Any


_PHASES = ((3, "en", r"\bthree[-\s]phase\s+AC\s+input\b"), (1, "en", r"\bsingle[-\s]phase\s+AC\s+input\b"),
           (3, "de", r"\b(?:drei|3)[-\s]?phasig(?:er|em|e|en)?\s+AC[-\s]Eingang\b"), (1, "de", r"\b(?:ein|1)[-\s]?phasig(?:er|em|e|en)?\s+AC[-\s]Eingang\b"),
           (3, "it", r"\b(?:ingresso\s+AC\s+trifase|ingresso\s+trifase\s+AC)\b"), (1, "it", r"\b(?:ingresso\s+AC\s+monofase|ingresso\s+monofase\s+AC|alimentazione\s+AC\s+monofase)\b"))
_DIN = (("en", r"\b(?:DIN\s+rail\s+mounting|mounted\s+on\s+(?:a\s+)?DIN\s+rail)\b"), ("de", r"\b(?:DIN[-\s]Schienenmontage|Montage\s+auf\s+(?:der\s+)?DIN[-\s]Schiene|Tragschienenmontage)\b"), ("it", r"\b(?:montaggio\s+su\s+(?:guida|barra)\s+DIN|installazione\s+su\s+guida\s+DIN)\b"))


def extract_claims(text: str) -> dict[str, Any]:
    """Recognize declared EN/DE/IT technical forms; never correct a fact."""
    result: dict[str, Any] = {}
    for value, language, pattern in _PHASES:
        match = re.search(pattern, text, re.I)
        if match:
            result["input_phase_count"] = {"attribute_id": "input_phase_count", "value": value, "unit": "phase", "surface_form": match.group(), "detected_language": language, "normalized_value": value, "normalized_unit": "phase"}
            break
    for language, pattern in _DIN:
        match = re.search(pattern, text, re.I)
        if match:
            result["mounting"] = {"attribute_id": "mounting", "value": "DIN_rail_NS35", "surface_form": match.group(), "detected_language": language, "normalized_concept": "DIN_RAIL"}
            break
    for attribute_id, unit, pattern in (("output_voltage", "V DC", r"(?<!\d)(\d+)\s*-?\s*V\s*-?\s*(?:D\s*-?\s*C|DC)(?!\w)"), ("nominal_output_current", "A", r"(?<!\w)(\d+)\s*-?\s*A(?!\w)")):
        match = re.search(pattern, text, re.I)
        if match:
            result[attribute_id] = {"attribute_id": attribute_id, "value": int(match.group(1)), "unit": unit, "surface_form": match.group(), "normalized_value": int(match.group(1)), "normalized_unit": unit}
    if match := re.search(r"\bNFC\b", text, re.I):
        result["interface"] = {"attribute_id": "interface", "value": "NFC", "surface_form": match.group(), "normalized_concept": "NFC"}
    return result
