"""Hash search simulation using the existing Grover demo as a conceptual engine."""
from typing import List, Optional, Tuple
import math

from utils.bitstring import normalize_bitstring, format_bitstring_output
import grover_algorithm as ga


def _index_to_bitstring(index: int, n_qubits: int) -> str:
    fmt = f"{index:0{n_qubits}b}"
    return fmt


def simulate_grover_hash_search(evidences: List[dict], suspect_hash: str, shots: int = 1000) -> Tuple[Optional[dict], float]:
    """Simulate a Grover-based search for an evidence by hash.

    Returns a tuple (evidence_dict or None, probability_of_measurement)
    """
    # Find target index (classical scan to define oracle)
    target_idx = None
    for i, e in enumerate(evidences):
        if e.get('hash') == suspect_hash:
            target_idx = i
            break

    if target_idx is None:
        return None, 0.0

    # Determine required qubits
    n_items = len(evidences)
    n_qubits = max(1, math.ceil(math.log2(max(2, n_items))))
    if n_qubits > 3:
        # For this demo, avoid creating large quantum circuits; fallback to classical
        return evidences[target_idx], 1.0

    # Build target bitstring in MSB-left convention
    target_bits = _index_to_bitstring(target_idx, n_qubits)

    # Normalize to internal Qiskit convention
    qiskit_target = normalize_bitstring(target_bits, n_qubits=n_qubits)

    # Build appropriate circuit using existing builders
    if n_qubits == 2:
        circuito = ga.criar_grover_2qubits(qiskit_target)
    else:
        try:
            from grover_advanced import grover_3qubits
            circuito = grover_3qubits(qiskit_target)
        except Exception:
            # Fallback to classical if builder not available
            return evidences[target_idx], 1.0

    # Execute circuit
    counts = ga.executar_grover(circuito, shots=shots)

    # Format counts for presentation (MSB-left)
    formatted = format_bitstring_output(counts, n_qubits=n_qubits)

    # Determine measurement probability for target
    prob = formatted.get(target_bits, 0) / max(1, sum(formatted.values()))

    return evidences[target_idx], prob
