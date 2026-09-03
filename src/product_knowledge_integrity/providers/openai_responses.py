"""Optional OpenAI Responses adapter for user-run experiments.

No key, historical response, customer prompt, or paid call is bundled with this project.
"""
from __future__ import annotations

import json
import os
import ssl
from typing import Any
from urllib.request import Request, urlopen

import certifi


def trusted_ssl_context() -> ssl.SSLContext:
    return ssl.create_default_context(cafile=certifi.where())


class OpenAIResponsesProvider:
    """Small opt-in adapter; callers supply their own key and decide whether to call it."""
    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5-mini")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def build_payload(self, text: str) -> dict[str, Any]:
        return {"model": self.model, "store": False, "input": text}

    def translate(self, text: str, source_language: str, target_language: str) -> str:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set; live usage is optional.")
        prompt = f"Translate technical product content from {source_language} to {target_language}. Preserve facts, numbers, units, and identifiers. Output only the translation.\n\n{text}"
        request = Request("https://api.openai.com/v1/responses", data=json.dumps(self.build_payload(prompt)).encode(), headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, method="POST")
        with urlopen(request, timeout=90, context=trusted_ssl_context()) as response:
            payload = json.load(response)
        return "".join(part.get("text", "") for item in payload.get("output", []) for part in item.get("content", []) if part.get("type") == "output_text")
