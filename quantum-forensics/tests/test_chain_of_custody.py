from forensic.chain_of_custody import ChainOfCustodyRecord


def test_chain_of_custody_same_content_same_hash():
    rec1 = ChainOfCustodyRecord(evidence_id='EV-001', created_by='tester')
    rec1.add_event('tester', 'create', 'initial', tool_version='1.0')
    h1 = rec1.finalize()

    rec2 = ChainOfCustodyRecord(evidence_id='EV-001', created_by='tester')
    rec2.add_event('tester', 'create', 'initial', tool_version='1.0')
    h2 = rec2.finalize()

    assert h1 == h2


def test_chain_of_custody_minimal_change_changes_hash():
    rec = ChainOfCustodyRecord(evidence_id='EV-001', created_by='tester')
    rec.add_event('tester', 'create', 'initial', tool_version='1.0')
    h1 = rec.finalize()
    rec.add_event('tester', 'modify', 'second', tool_version='1.0')
    h2 = rec.finalize()
    assert h1 != h2


if __name__ == '__main__':
    test_chain_of_custody_same_content_same_hash()
    test_chain_of_custody_minimal_change_changes_hash()
    print('test_chain_of_custody passed')
