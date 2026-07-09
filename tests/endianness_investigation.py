"""Investigation script for Qiskit endianness behavior.

This script tests all 2-qubit and 3-qubit target states by constructing Grover
circuits from the project's modules, running them on AerSimulator, and
comparing the requested target state with the most probable measured state.
"""

from math import sqrt, pi
import os
import sys
from qiskit_aer import AerSimulator

# Ensure project root is on sys.path so imports work when running from tests/
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from grover_algorithm import criar_grover_2qubits
from grover_advanced import grover_3qubits

SIMULATOR = AerSimulator()
SHOTS = 2000


def run_test_2qubits():
    states = [f"{i:02b}" for i in range(4)]
    results = []
    for target in states:
        circuito = criar_grover_2qubits(target)
        job = SIMULATOR.run(circuito, shots=SHOTS)
        resultado = job.result()
        counts = resultado.get_counts(circuito)
        # Find most probable measured state
        measured = max(counts.items(), key=lambda x: x[1])[0]
        results.append((target, measured, counts))
    return results


def run_test_3qubits():
    states = [f"{i:03b}" for i in range(8)]
    results = []
    N = 8
    # optimal iterations ~ pi/4 * sqrt(N)
    opt_iters = max(1, round((pi/4) * sqrt(N)))
    for target in states:
        circuito = grover_3qubits(target, num_iteracoes=opt_iters)
        job = SIMULATOR.run(circuito, shots=SHOTS)
        resultado = job.result()
        counts = resultado.get_counts(circuito)
        measured = max(counts.items(), key=lambda x: x[1])[0]
        results.append((target, measured, counts))
    return results


def analyze(results):
    lines = []
    for target, measured, counts in results:
        reversed_target = target[::-1]
        ok = measured == target
        reversed_ok = measured == reversed_target
        lines.append({
            'target': target,
            'measured': measured,
            'reversed_target': reversed_target,
            'match': ok,
            'match_reversed': reversed_ok,
            'top_count': counts[measured],
            'total_shots': sum(counts.values())
        })
    return lines


def main():
    print('Running 2-qubit tests...')
    res2 = run_test_2qubits()
    analysis2 = analyze(res2)

    print('\n2-qubit results:')
    for r in analysis2:
        print(r)

    print('\nRunning 3-qubit tests...')
    res3 = run_test_3qubits()
    analysis3 = analyze(res3)

    print('\n3-qubit results:')
    for r in analysis3:
        print(r)

    # Write a short report
    with open('REPORT_ENDIANNESS.md', 'w') as f:
        f.write('# Endianness Investigation Report\n\n')
        f.write('2-qubit results\n')
        for r in analysis2:
            f.write(str(r) + '\n')
        f.write('\n3-qubit results\n')
        for r in analysis3:
            f.write(str(r) + '\n')

    print('\nReport written to REPORT_ENDIANNESS.md')


if __name__ == '__main__':
    main()
