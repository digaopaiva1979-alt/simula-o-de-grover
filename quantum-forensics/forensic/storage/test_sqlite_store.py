from __future__ import annotations
import json
import tempfile

from forensic.storage.sqlite_store import SqliteForensicStore
from forensic.models.evidence import Evidence
from forensic.chain_of_custody import ChainOfCustodyRecord


def test_sqlite_store_crud_and_export(tmp_path):
    db_path = tmp_path / 'forensic.db'
    store = SqliteForensicStore(str(db_path))

    store.upsert_case('CASE-001', 'Analista Silva')

    evidence = Evidence.create(
        id='EV-999',
        filename='test.bin',
        sha256='deadbeef',
        source='disk.dd',
        metadata={'size': '1234', 'description': 'teste'},
    )
    store.save_evidence('CASE-001', evidence)

    record = ChainOfCustodyRecord(evidence_id='EV-999', created_by='Analista Silva')
    record.add_event('analyst', 'evidence_collected', 'Evidence ingested for test', tool_version='quantum-forensics/test')
    store.save_chain_of_custody(record)

    case_data = store.load_case('CASE-001')
    assert case_data is not None
    assert case_data['case_id'] == 'CASE-001'
    assert len(case_data['evidences']) == 1
    assert case_data['evidences'][0].id == 'EV-999'
    assert case_data['chain_of_custody'][0].record_hash == record.record_hash

    json_path = tmp_path / 'case_export.json'
    store.export_case_json('CASE-001', str(json_path))
    exported = json.loads(json_path.read_text(encoding='utf-8'))
    assert exported['case_id'] == 'CASE-001'
    assert exported['evidences'][0]['sha256'] == 'deadbeef'

    store.close()
