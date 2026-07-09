from forensic.chain_of_custody import ChainOfCustodyRecord


def test_chain_of_custody_finalize():
    rec = ChainOfCustodyRecord(evidence_id='EV-001', created_by='tester')
    rec.add_event('tester', 'create', 'initial')
    h1 = rec.finalize()
    assert isinstance(h1, str) and len(h1) == 64
    # Add another event and ensure hash changes
    rec.add_event('tester', 'modify', 'second')
    h2 = rec.finalize()
    assert h1 != h2


if __name__ == '__main__':
    test_chain_of_custody_finalize()
    print('test_chain_of_custody passed')
