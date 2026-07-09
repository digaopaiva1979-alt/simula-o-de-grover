from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from ..storage.repositories import CaseRepository


def export_case_stix(repository: CaseRepository, case_id: str, output_path: str) -> None:
    case = repository.get_case(case_id)
    if case is None:
        raise ValueError(f"Case {case_id} not found")

    bundle = {
        "type": "bundle",
        "id": f"bundle--{case.case_id}",
        "objects": [
            {
                "type": "note",
                "id": f"note--{case.case_id}",
                "created": case.created_at,
                "modified": case.updated_at,
                "abstract": case.title,
                "content": case.description,
            }
        ],
    }

    for evidence in case.evidences:
        bundle["objects"].append(
            {
                "type": "artifact",
                "id": f"artifact--{evidence.evidence_id}",
                "name": evidence.filename,
                "hashes": {"SHA-256": evidence.sha256},
                "mime_type": "application/octet-stream",
            }
        )

    for ioc in case.iocs:
        bundle["objects"].append(
            {
                "type": "indicator",
                "id": f"indicator--{ioc.ioc_id}",
                "pattern": f"[file:hashes.'SHA-256' = '{ioc.value}']",
                "valid_from": ioc.created_at,
            }
        )

    Path(output_path).write_text(json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8")
