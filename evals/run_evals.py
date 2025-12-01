"""Simple evaluation runner for the Florida Retirement Resources system.

This script:
- Loads test cases from evals/health_review/multi_domain_v1.jsonl
- Runs each input through the coordinator via RetirementResourcesApp
- Applies cheap automatic checks (safety/content heuristics)
- Prints a compact summary and exits non-zero if there are hard failures
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from main import RetirementResourcesApp


EVAL_FILE = Path(__file__).parent / "health_review" / "multi_domain_v1.jsonl"


@dataclass
class EvalCase:
    id: str
    input: str
    intent_type: str
    expected_domains: List[str]
    must_contain: List[str]
    must_not_contain: List[str]
    raw: Dict[str, Any]


def load_cases(path: Path) -> List[EvalCase]:
    cases: List[EvalCase] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            cases.append(
                EvalCase(
                    id=data["id"],
                    input=data["input"],
                    intent_type=data.get("intent_type", "unknown"),
                    expected_domains=data.get("expected_domains", []),
                    must_contain=data.get("must_contain", []),
                    must_not_contain=data.get("must_not_contain", []),
                    raw=data,
                )
            )
    return cases


def text_contains_all(text: str, snippets: List[str]) -> bool:
    return all(snippet.lower() in text.lower() for snippet in snippets)


def text_contains_any(text: str, snippets: List[str]) -> bool:
    return any(snippet.lower() in text.lower() for snippet in snippets)


def run_evals() -> int:
    if not EVAL_FILE.exists():
        raise FileNotFoundError(f"Eval file not found: {EVAL_FILE}")

    cases = load_cases(EVAL_FILE)
    app = RetirementResourcesApp()

    total = len(cases)
    hard_failures: List[str] = []
    soft_warnings: List[str] = []

    print(f"Loaded {total} evaluation cases from {EVAL_FILE}")

    for case in cases:
        print(f"\n=== Case {case.id} ===")
        print(f"Input: {case.input}")

        response = app.chat(case.input, session_id=f"eval_{case.id}")
        print(f"Response:\n{response}\n")

        # Hard checks: must_contain / must_not_contain
        failed = False
        if case.must_contain and not text_contains_all(response, case.must_contain):
            print(f"[FAIL] Missing one or more required phrases in response.")
            hard_failures.append(case.id)
            failed = True

        if case.must_not_contain and text_contains_any(response, case.must_not_contain):
            print(f"[FAIL] Response contains banned phrase.")
            if case.id not in hard_failures:
                hard_failures.append(case.id)
            failed = True

        # Soft heuristic: for multi_domain, ensure at least two key terms appear
        if case.intent_type == "multi_domain":
            # Simple heuristic keywords for domains
            medicare_present = bool(re.search(r"\bmedicare\b", response, re.IGNORECASE))
            medicaid_present = bool(re.search(r"\bmedicaid\b", response, re.IGNORECASE))
            city_hint = case.raw.get("profile_hints", {}).get("city")
            city_present = bool(
                city_hint
                and re.search(rf"\b{re.escape(str(city_hint))}\b", response, re.IGNORECASE)
            )
            if not (medicare_present and medicaid_present and city_present):
                msg = (
                    f"[WARN] multi_domain case '{case.id}' did not obviously mention "
                    f"Medicare, Medicaid, and city '{city_hint}'."
                )
                print(msg)
                soft_warnings.append(msg)

        if not failed:
            print("[OK] All hard checks passed for this case.")

    print("\n=== Evaluation Summary ===")
    print(f"Total cases: {total}")
    print(f"Hard failures: {len(hard_failures)}")
    if hard_failures:
        print("Failed case IDs:", ", ".join(hard_failures))
    print(f"Warnings: {len(soft_warnings)}")

    # Non-zero exit code if we have hard failures (for CI)
    return 1 if hard_failures else 0


if __name__ == "__main__":
    raise SystemExit(run_evals())


