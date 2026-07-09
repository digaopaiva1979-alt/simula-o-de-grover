"""Quantum interface adapter for the forensic package.

This module encapsulates interactions with the project's Grover builders and
executors. Forensic modules should call `simulate_search()` and not import
Qiskit or Grover builder functions directly.
"""
from typing import List, Optional, Tuple
import math

from utils.bitstring import normalize_bitstring, format_bitstring_output
import grover_algorithm as ga


def _index_to_bitstring(index: int, n_qubits: int) -> str:
    return f"{index:0{n_qubits}b}"


def simulate_search(evidences: List[dict], suspect_hash: str, shots: int = 1000) -> Tuple[Optional[dict], float]:
    """Simulate a search for an evidence by suspect_hash using Grover as a
    conceptual engine.

    Returns (found_evidence_dict or None, measured_probability)
    """
    # Locate target index classically to define the oracle target
    target_idx = None
    for i, e in enumerate(evidences):
        if e.get('hash') == suspect_hash:
            target_idx = i
            break
    if target_idx is None:
        return None, 0.0

    n_items = len(evidences)
    n_qubits = max(1, math.ceil(math.log2(max(2, n_items))))

    # For safety in this demo, avoid constructing circuits >3 qubits
    if n_qubits > 3:
        return evidences[target_idx], 1.0

    # Map index to MSB-left bitstring
    target_bits = _index_to_bitstring(target_idx, n_qubits)

    # Normalize to Qiskit convention (adapter responsibility)
    qiskit_target = normalize_bitstring(target_bits, n_qubits=n_qubits)

    # Build circuit via project builders
    if n_qubits == 2:
        circuito = ga.criar_grover_2qubits(qiskit_target)
    else:
        try:
            from grover_advanced import grover_3qubits
            circuito = grover_3qubits(qiskit_target)
        except Exception:
            return evidences[target_idx], 1.0

    counts = ga.executar_grover(circuito, shots=shots)

    formatted = format_bitstring_output(counts, n_qubits=n_qubits)

    prob = formatted.get(target_bits, 0) / max(1, sum(formatted.values()))

    return evidences[target_idx], prob
