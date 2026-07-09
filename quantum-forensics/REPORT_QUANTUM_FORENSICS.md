REPORT — Quantum Forensic Search Simulator

Architecture

- `quantum-forensics/forensic`: package with modules for evidences, IOC database,
  hash search (integration with Grover demo), malware signature simulation and
  chain-of-custody representation.
- `quantum-forensics/exemplos/caso_forense_simulado.py`: end-to-end demo script.
- `quantum-forensics/docs/QUANTUM_FORENSICS.md`: documentation and limitations.

Files added

- forensic/__init__.py
- forensic/evidencias.py
- forensic/ioc_database.py
- forensic/hash_search.py
- forensic/malware_signature.py
- forensic/chain_of_custody.py
- exemplos/caso_forense_simulado.py
- docs/QUANTUM_FORENSICS.md

Decisions and rationale

- Kept Grover algorithm code untouched; used existing builders in `grover_algorithm.py`
  and `grover_advanced.py` to construct circuits for 2-3 qubit demonstrations.
- For larger item sets (>3 qubits) the simulator falls back to a classical
  resolution to avoid constructing large circuits in this demo.
- `format_bitstring_output()` and `normalize_bitstring()` from `utils/bitstring.py`
  are used as adapters between user-oriented bitstring representation and the
  Qiskit convention.

Limitations

- Educational only: not suitable for real forensic usage.
- Only small datasets are executed quantumly.

Next steps

- Expand builders to generically support n-qubits if desired (requires
  careful testing and potential refactor of quantum builders).
- Add richer simulation of noise and measurement uncertainty.
- Provide richer example cases and link to CI smoke tests.
