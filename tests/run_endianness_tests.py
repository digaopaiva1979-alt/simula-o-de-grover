"""Run endianness tests without pytest (for environments without pytest).

Exit code 0 on success, non-zero on failure.
"""
import os
import sys
from math import sqrt, pi

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from qiskit_aer import AerSimulator
from utils.bitstring import normalize_bitstring
from grover_algorithm import criar_grover_2qubits
from grover_advanced import grover_3qubits

SIM = AerSimulator()
SHOTS = 1000

failures = []

# 2-qubit tests
for i in range(4):
    target = f"{i:02b}"
    q_target = normalize_bitstring(target, n_qubits=2)
    circuito = criar_grover_2qubits(q_target)
    job = SIM.run(circuito, shots=SHOTS)
    res = job.result()
    counts = res.get_counts(circuito)
    measured = max(counts.items(), key=lambda x: x[1])[0]
    if measured != target:
        failures.append((target, measured))

# 3-qubit tests
N = 8
opt_iters = max(1, round((pi/4) * sqrt(N)))
for i in range(8):
    target = f"{i:03b}"
    q_target = normalize_bitstring(target, n_qubits=3)
    circuito = grover_3qubits(q_target, num_iteracoes=opt_iters)
    job = SIM.run(circuito, shots=SHOTS)
    res = job.result()
    counts = res.get_counts(circuito)
    measured = max(counts.items(), key=lambda x: x[1])[0]
    if measured != target:
        failures.append((target, measured))

if failures:
    print('Some tests failed:')
    for t, m in failures:
        print(f'  target={t} measured={m}')
    sys.exit(2)

print('All endianness normalization tests passed.')
sys.exit(0)
