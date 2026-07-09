from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from ..storage.repositories import CaseRepository


def export_case_json(repository: CaseRepository, case_id: str, output_path: str) -> None:
    case = repository.get_case(case_id)
    if case is None:
        raise ValueError(f"Case {case_id} not found")

    payload = case.to_dict()
    Path(output_path).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
