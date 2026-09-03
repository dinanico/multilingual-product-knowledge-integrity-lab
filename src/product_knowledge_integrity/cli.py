from __future__ import annotations

import argparse
import json

from .io import write_json
from .pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the deterministic product knowledge integrity demo.")
    parser.add_argument("--dataset", required=True, help="Path to a fictional dataset directory")
    parser.add_argument("--phase", choices=["baseline", "retest"], default="baseline")
    parser.add_argument("--output", help="Optional local JSON output path")
    args = parser.parse_args()
    result = run_pipeline(args.dataset, args.phase)
    if args.output:
        write_json(args.output, result)
    print(json.dumps({"phase": result["phase"], "publication_gate": result["publication_gate"], "ai_evaluation": result["ai_evaluation"]["summary"], "root_causes": result["root_causes"]}, indent=2))


if __name__ == "__main__":
    main()
