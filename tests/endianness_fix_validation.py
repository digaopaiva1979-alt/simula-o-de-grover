"""Validate endianness fix by reversing target strings before building circuits.

This script runs 2-qubit and 3-qubit tests where we pass the reversed target
string to the existing circuit builders and assert that the measured top state
matches the original (non-reversed) target.
"""

from math import sqrt, pi
import os
import sys
from qiskit_aer import AerSimulator

# Ensure project root on path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from grover_algorithm import criar_grover_2qubits
from grover_advanced import grover_3qubits

SIMULATOR = AerSimulator()
SHOTS = 2000


def test_with_reversed_input_2qubits():
    states = [f"{i:02b}" for i in range(4)]
    results = []
    for target in states:
        reversed_target = target[::-1]
        circuito = criar_grover_2qubits(reversed_target)
        job = SIMULATOR.run(circuito, shots=SHOTS)
        resultado = job.result()
        counts = resultado.get_counts(circuito)
        measured = max(counts.items(), key=lambda x: x[1])[0]
        success = measured == target
        results.append((target, reversed_target, measured, success))
    return results


def test_with_reversed_input_3qubits():
    states = [f"{i:03b}" for i in range(8)]
    results = []
    N = 8
    opt_iters = max(1, round((pi/4) * sqrt(N)))
    for target in states:
        reversed_target = target[::-1]
        circuito = grover_3qubits(reversed_target, num_iteracoes=opt_iters)
        job = SIMULATOR.run(circuito, shots=SHOTS)
        resultado = job.result()
        counts = resultado.get_counts(circuito)
        measured = max(counts.items(), key=lambda x: x[1])[0]
        success = measured == target
        results.append((target, reversed_target, measured, success))
    return results


def main():
    print('Running fix validation for 2 qubits...')
    res2 = test_with_reversed_input_2qubits()
    for r in res2:
        print(r)

    print('\nRunning fix validation for 3 qubits...')
    res3 = test_with_reversed_input_3qubits()
    for r in res3:
        print(r)

    with open('REPORT_ENDIANNESS.md', 'a') as f:
        f.write('\n\n---\n\nValidation of reversed-input fix:\n')
        f.write('\n2-qubit validation:\n')
        for r in res2:
            f.write(str(r) + '\n')
        f.write('\n3-qubit validation:\n')
        for r in res3:
            f.write(str(r) + '\n')

    print('\nValidation appended to REPORT_ENDIANNESS.md')


if __name__ == '__main__':
    main()
