"""Hash search facade that delegates to a quantum interface adapter.

This module exposes a simple function for higher-level forensic code to
request a hash-based search over a list of evidences. The implementation
delegates the quantum/back-end details to `quantum_interface` so forensic
modules do not import Qiskit directly.
"""
from typing import Iterable, Optional, Tuple, Union

from .models.evidence import Evidence
from .quantum_interface import simulate_search


def simulate_grover_hash_search(
    evidences: Iterable[Union[Evidence, dict]],
    suspect_hash: str,
    shots: int = 1000,
) -> Tuple[Optional[Union[Evidence, dict]], float]:
    """Facade that delegates to the quantum interface adapter.

    Returns (evidence or None, probability)
    """
    return simulate_search(list(evidences), suspect_hash, shots=shots)
