from __future__ import annotations
import json
from pathlib import Path

from forensic.storage import SqliteForensicStore
from forensic.models.evidence import Evidence
from forensic.chain_of_custody import ChainOfCustodyRecord
from forensic.exporters import export_case_json, export_case_stix
from forensic.graph import export_graph_json
from forensic.case import ForensicCase


def test_exporters_and_graph_json(tmp_path):
    db_path = tmp_path / 'forensic.db'
    store = SqliteForensicStore(str(db_path))
    store.upsert_case('CASE-002', 'Investigador Souza')

    evidence = Evidence.create(
        id='EV-1000',
        filename='sample.bin',
        sha256='5d41402a',
        source='image.dd',
        metadata={'notes': 'artifact'},
    )
    store.save_evidence('CASE-002', evidence)

    record = ChainOfCustodyRecord(evidence_id='EV-1000', created_by='Investigador Souza')
    record.add_event('analyst', 'collected', 'Evidence added to case', tool_version='quantum-forensics/test')
    store.save_chain_of_custody(record)

    json_path = tmp_path / 'case_export.json'
    export_case_json(store, 'CASE-002', str(json_path))
    exported = json.loads(Path(json_path).read_text(encoding='utf-8'))
    assert exported['case_id'] == 'CASE-002'
    assert exported['evidences'][0]['id'] == 'EV-1000'

    stix_path = tmp_path / 'case_export.stix.json'
    export_case_stix(store, 'CASE-002', str(stix_path))
    stix_data = json.loads(Path(stix_path).read_text(encoding='utf-8'))
    assert stix_data['type'] == 'bundle'
    assert any(obj['type'] == 'artifact' for obj in stix_data['objects'])

    case = ForensicCase(case_id='CASE-002', investigator='Investigador Souza')
    case.evidences.append(evidence)
    case.chain_of_custody.append(record)

    graph_path = tmp_path / 'case_graph.json'
    export_graph_json(case, str(graph_path))
    graph_data = json.loads(Path(graph_path).read_text(encoding='utf-8'))
    assert graph_data['nodes']
    assert graph_data['edges']

    store.close()
