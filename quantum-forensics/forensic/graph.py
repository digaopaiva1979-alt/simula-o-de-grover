from __future__ import annotations

import json
from typing import Any, Dict, List

from .case import ForensicCase


def build_investigation_graph(case: ForensicCase) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    nodes.append({
        'id': case.case_id,
        'type': 'case',
        'label': f'Case {case.case_id}',
        'investigator': case.investigator,
        'created_at': case.created_at,
        'updated_at': case.updated_at,
    })

    for evidence in case.evidences:
        nodes.append({
            'id': evidence.id,
            'type': 'evidence',
            'label': evidence.filename,
            'sha256': evidence.sha256,
            'source': evidence.source,
        })
        edges.append({
            'source': case.case_id,
            'target': evidence.id,
            'relation': 'contains',
        })

    if case.indicators_found:
        for indicator_type in ('hash', 'ip', 'domain'):
            indicator_value = getattr(case.indicators_found, indicator_type)
            if indicator_value:
                indicator_id = f'{case.case_id}-{indicator_type}-{indicator_value}'
                nodes.append({
                    'id': indicator_id,
                    'type': 'indicator',
                    'indicator_type': indicator_type,
                    'value': indicator_value,
                })
                edges.append({
                    'source': case.case_id,
                    'target': indicator_id,
                    'relation': 'observed_in',
                })
                for evidence_id in case.indicators_found.related_evidence_ids:
                    edges.append({
                        'source': indicator_id,
                        'target': evidence_id,
                        'relation': 'related_to',
                    })

    for index, event in enumerate(case.timeline):
        event_id = event.get('event_id') or f'{case.case_id}-event-{index}'
        nodes.append({
            'id': event_id,
            'type': 'timeline_event',
            'description': event.get('description', ''),
            'timestamp_utc': event.get('timestamp_utc', ''),
            'details': event.get('details', {}),
        })
        edges.append({
            'source': case.case_id,
            'target': event_id,
            'relation': 'timeline',
        })

    for record in case.chain_of_custody:
        record_id = record.record_hash or f'{case.case_id}-record-{record.evidence_id}'
        nodes.append({
            'id': record_id,
            'type': 'custody_record',
            'evidence_id': record.evidence_id,
            'created_by': record.created_by,
            'created_at': record.created_at,
            'schema_version': record.schema_version,
            'hash_algo': record.hash_algo,
        })
        edges.append({
            'source': record.evidence_id,
            'target': record_id,
            'relation': 'custody_chain',
        })

    return {
        'nodes': nodes,
        'edges': edges,
    }


def export_graph_json(case: ForensicCase, output_path: str) -> None:
    graph = build_investigation_graph(case)
    with open(output_path, 'w', encoding='utf-8') as handle:
        json_text = json.dumps(graph, indent=2, sort_keys=True)
        handle.write(json_text)
