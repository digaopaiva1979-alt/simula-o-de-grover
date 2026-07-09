from forensic.chain_of_custody import ChainOfCustodyRecord


def test_chain_of_custody_deterministic_hash():
    fixed_timestamp = '2026-07-09T00:00:00Z'
    rec1 = ChainOfCustodyRecord(evidence_id='EV-001', created_by='tester', created_at=fixed_timestamp)
    rec1.add_event('tester', 'create', 'initial', tool_version='1.0', timestamp_utc=fixed_timestamp)
    h1 = rec1.finalize()

    rec2 = ChainOfCustodyRecord(evidence_id='EV-001', created_by='tester', created_at=fixed_timestamp)
    rec2.add_event('tester', 'create', 'initial', tool_version='1.0', timestamp_utc=fixed_timestamp)
    h2 = rec2.finalize()

    assert h1 == h2


def test_chain_of_custody_change_changes_hash():
    fixed_timestamp = '2026-07-09T00:00:00Z'
    rec = ChainOfCustodyRecord(evidence_id='EV-001', created_by='tester', created_at=fixed_timestamp)
    rec.add_event('tester', 'create', 'initial', tool_version='1.0', timestamp_utc=fixed_timestamp)
    h1 = rec.finalize()
    rec.add_event('tester', 'modify', 'second', tool_version='1.0', timestamp_utc=fixed_timestamp)
    h2 = rec.finalize()
    assert h1 != h2


if __name__ == '__main__':
    test_chain_of_custody_deterministic_hash()
    test_chain_of_custody_change_changes_hash()
    print('test_chain_of_custody_deterministic passed')
