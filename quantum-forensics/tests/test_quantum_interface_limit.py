from forensic.backends import QuantumSimulationLimitError
from forensic.quantum_interface import simulate_search
from forensic.evidencias import sample_evidences


def test_simulate_search_limit():
    evidences = sample_evidences() * 5
    try:
        simulate_search(evidences, 'deadbeef', shots=10)
        assert False, 'QuantumSimulationLimitError should have been raised'
    except QuantumSimulationLimitError:
        assert True


if __name__ == '__main__':
    test_simulate_search_limit()
    print('test_quantum_interface_limit passed')
