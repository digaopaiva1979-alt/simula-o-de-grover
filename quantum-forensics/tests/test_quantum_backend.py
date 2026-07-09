from forensic.backends.qiskit_backend import QiskitBackend, QuantumSimulationLimitError
from forensic.evidencias import sample_evidences


def test_qiskit_backend_build_and_execute():
    backend = QiskitBackend()
    evidences = sample_evidences()
    target = '01'
    circuit = backend.build_search(evidences, target)
    counts = backend.execute(circuit, shots=10)
    assert isinstance(counts, dict)
    assert all(isinstance(k, str) for k in counts.keys())
    assert sum(counts.values()) == 10


def test_qiskit_backend_exceeds_limit():
    backend = QiskitBackend()
    evidences = sample_evidences() + sample_evidences() + sample_evidences() + sample_evidences()
    try:
        backend.build_search(evidences, '0000')
        assert False, 'QuantumSimulationLimitError should have been raised'
    except QuantumSimulationLimitError:
        assert True


if __name__ == '__main__':
    test_qiskit_backend_build_and_execute()
    test_qiskit_backend_exceeds_limit()
    print('test_qiskit_backend passed')
