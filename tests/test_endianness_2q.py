import os
import sys
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from qiskit_aer import AerSimulator
from utils.bitstring import normalize_bitstring
from grover_algorithm import criar_grover_2qubits

SIM = AerSimulator()
SHOTS = 1000


@pytest.mark.parametrize('target', [f"{i:02b}" for i in range(4)])
def test_2q_target_is_amplified(target):
    qiskit_target = normalize_bitstring(target, n_qubits=2)
    circuito = criar_grover_2qubits(qiskit_target)
    job = SIM.run(circuito, shots=SHOTS)
    res = job.result()
    counts = res.get_counts(circuito)
    measured = max(counts.items(), key=lambda x: x[1])[0]
    assert measured == target, f"For target {target}, measured {measured}"
