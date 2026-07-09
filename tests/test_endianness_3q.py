import os
import sys
import pytest
from math import sqrt, pi

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from qiskit_aer import AerSimulator
from utils.bitstring import normalize_bitstring
from grover_advanced import grover_3qubits

SIM = AerSimulator()
SHOTS = 1000


@pytest.mark.parametrize('target', [f"{i:03b}" for i in range(8)])
def test_3q_target_is_amplified(target):
    qiskit_target = normalize_bitstring(target, n_qubits=3)
    # optimal iterations ~ pi/4 * sqrt(N)
    N = 8
    opt_iters = max(1, round((pi/4) * sqrt(N)))
    circuito = grover_3qubits(qiskit_target, num_iteracoes=opt_iters)
    job = SIM.run(circuito, shots=SHOTS)
    res = job.result()
    counts = res.get_counts(circuito)
    measured = max(counts.items(), key=lambda x: x[1])[0]
    assert measured == target, f"For target {target}, measured {measured}"
