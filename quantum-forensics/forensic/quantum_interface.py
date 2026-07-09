"""Quantum interface adapter for the forensic package.

This module encapsulates interactions between forensic code and a quantum
backend. Forensic modules should call `simulate_search()` and not import
Qiskit or Grover builder functions directly.
"""
from __future__ import annotations

from typing import Any, Iterable, List, Optional, Tuple
import math

from .backends import QiskitBackend, QuantumBackend, QuantumSimulationLimitError


def _index_to_bitstring(index: int, n_qubits: int) -> str:
    return f"{index:0{n_qubits}b}"


def _extract_hash(evidence: Any) -> Optional[str]:
    if isinstance(evidence, dict):
        return evidence.get('sha256') or evidence.get('hash')
    return getattr(evidence, 'sha256', None)


def simulate_search(
    evidences: List[Any],
    suspect_hash: str,
    shots: int = 1000,
    backend: Optional[QuantumBackend] = None,
) -> Tuple[Optional[Any], float]:
    """Simulate a search for an evidence by suspect hash using a quantum backend.

    Returns (found_evidence or None, measured_probability)
    """
    if backend is None:
        backend = QiskitBackend()

    target_idx = None
    for i, evidence in enumerate(evidences):
        if _extract_hash(evidence) == suspect_hash:
            target_idx = i
            break
    if target_idx is None:
        return None, 0.0

    n_items = len(evidences)
    n_qubits = max(1, math.ceil(math.log2(max(2, n_items))))
    target_bits = _index_to_bitstring(target_idx, n_qubits)

    circuit = backend.build_search(evidences, target_bits)
    counts = backend.execute(circuit, shots=shots)

    prob = counts.get(target_bits, 0) / max(1, sum(counts.values()))
    return evidences[target_idx], prob
