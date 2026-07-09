from forensic.models.evidence import Evidence


def test_evidence_model_create_and_to_dict():
    evidence = Evidence.create(
        id='EV-100',
        filename='sample.bin',
        sha256='deadbeef',
        source='image.dd',
        metadata={'size': '1MB'},
    )
    data = evidence.to_dict()
    assert data['id'] == 'EV-100'
    assert data['sha256'] == 'deadbeef'
    assert data['source'] == 'image.dd'
    assert 'collected_at' in data


if __name__ == '__main__':
    test_evidence_model_create_and_to_dict()
    print('test_evidence_model passed')
