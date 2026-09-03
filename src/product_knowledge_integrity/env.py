from __future__ import annotations

import os
from pathlib import Path


def load_env_file(path: str | Path = ".env") -> None:
    """Load simple local KEY=VALUE entries without overriding shell variables."""
    candidate = Path(path)
    if not candidate.is_file():
        return
    for line in candidate.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())
