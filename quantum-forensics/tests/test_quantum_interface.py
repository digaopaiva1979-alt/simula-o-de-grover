from forensic.evidencias import to_dict_list, sample_evidences
from forensic.quantum_interface import simulate_search


def test_quantum_interface_found():
    evid = sample_evidences()
    evid_list = to_dict_list(evid)
    # pick a known hash from sample evidences
    suspect = evid_list[3]['sha256']
    found, prob = simulate_search(evid_list, suspect, shots=100)
    assert found is not None
    assert prob >= 0.0 and prob <= 1.0


if __name__ == '__main__':
    test_quantum_interface_found()
    print('test_quantum_interface passed')
