from forensic.case import ForensicCase, ForensicPipeline
from forensic.evidencias import sample_evidences


def main():
    evidences = sample_evidences()
    case = ForensicCase(case_id='CASE-001', investigator='Analista Silva')
    pipeline = ForensicPipeline(case)

    pipeline.collect_evidence(evidences)
    pipeline.analyze_hashes()

    observed = {
        'hash': evidences[3].sha256,
        'ip': '192.168.1.10',
        'domain': 'malware.test',
        'source': 'imagem_forense.dd',
    }

    pipeline.correlate_iocs(observed)
    pipeline.calculate_risk()
    pipeline.run_quantum_search(shots=500)
    report = pipeline.generate_report()

    print(report)


if __name__ == '__main__':
    main()
