from forensic.case import ForensicCase, ForensicPipeline
from forensic.evidencias import sample_evidences


def test_forensic_pipeline_end_to_end():
    evidences = sample_evidences()
    case = ForensicCase(case_id='CASE-001', investigator='Analista Silva')
    pipeline = ForensicPipeline(case)

    pipeline.collect_evidence(evidences)
    hashes = pipeline.analyze_hashes()
    assert evidences[0].sha256 in hashes

    observed = {
        'hash': evidences[3].sha256,
        'ip': '192.168.1.10',
        'domain': 'malware.test',
        'source': 'imagem_forense.dd',
    }

    correlation = pipeline.correlate_iocs(observed)
    assert 'hash:deadbeef' in correlation.matched_iocs

    risk = pipeline.calculate_risk()
    assert risk['total_score'] >= 0

    result = pipeline.run_quantum_search(shots=100)
    assert result['probability'] >= 0.0
    assert case.chain_of_custody

    report = pipeline.generate_report()
    assert 'Case ID: CASE-001' in report
    assert 'Quantum Search Result:' in report


if __name__ == '__main__':
    test_forensic_pipeline_end_to_end()
    print('test_forensic_pipeline passed')
