# Quantum Forensics Simulator (Academic Demo)

This document explains the scope and limitations of the Quantum Forensic Search
Simulator included in this project.

Scope

- Academic simulation that demonstrates how a quantum search (Grover) could
  be conceptually applied to search for indicators of compromise within a set
  of digital evidences.

Limitations

- This is a toy simulation. The Grover-based flows are executed on local
  simulators (Qiskit Aer) and are constrained to small item sets (2-3 qubits)
  for demonstration.
- No real forensic procedures are implemented — the module illustrates
  conceptual mapping between indices and bitstrings and should not be used in
  production forensic workflows.

Classical vs Quantum search

- Classical search inspects items one-by-one (O(N)).
- Grover provides a quadratic speedup conceptually (O(√N)). In this project,
  the quantum execution is kept small to illustrate behavior and measurement
  probabilities.

Hardware considerations

- Current quantum hardware is limited in qubit counts and noise levels. Our
  simulation does not model noise robustly; results are for educational purposes.

Perícia digital

- The simulator demonstrates a mapping where each evidence is assigned an
  index mapped to a bitstring; the Grover oracle conceptually marks the index
  matching a suspect IOC (hash) and the circuit amplifies its amplitude.
- A real forensic workflow requires careful chain-of-custody, validated
  hashing, legal procedures and reproducible tooling — this demo stays strictly
  academic.
