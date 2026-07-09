from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional

from .storage.sqlite_store import SqliteForensicStore


def export_case_json(store: SqliteForensicStore, case_id: str, output_path: str) -> None:
    store.export_case_json(case_id, output_path)


def export_case_stix(store: SqliteForensicStore, case_id: str, output_path: str) -> None:
    case_data = store.load_case(case_id)
    if case_data is None:
        raise ValueError(f'Case {case_id} not found')

    # Very small STIX 2.1-compatible payload for demonstration purposes.
    stix_bundle = {
        'type': 'bundle',
        'id': f'bundle--{case_id}',
        'objects': [],
    }

    case_obj = {
        'type': 'note',
        'id': f'note--{case_id}',
        'created': case_data['created_at'],
        'modified': case_data['updated_at'],
        'abstract': f'Forensic case {case_id} led by {case_data["investigator"]}',
        'content': f'Investigator: {case_data["investigator"]}',
    }
    stix_bundle['objects'].append(case_obj)

    for evidence in case_data.get('evidences', []):
        stix_bundle['objects'].append({
            'type': 'artifact',
            'id': f'artifact--{evidence.id}',
            'name': evidence.filename,
            'hashes': {'SHA-256': evidence.sha256},
            'mime_type': 'application/octet-stream',
            'payload_bin': None,
        })

    if case_data.get('ioc_correlation'):
        stix_bundle['objects'].append({
            'type': 'indicator',
            'id': f'indicator--{case_id}',
            'pattern': ' OR '.join([f"[file:hashes.'SHA-256' = '{h}']" for h in case_data['ioc_correlation'].get('matched_iocs', [])]),
            'valid_from': case_data['updated_at'],
        })

    Path(output_path).write_text(json.dumps(stix_bundle, indent=2, sort_keys=True), encoding='utf-8')
