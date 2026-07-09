from __future__ import annotations
import math
from typing import Any, Dict, Iterable

from utils.bitstring import normalize_bitstring, format_bitstring_output
from .quantum_backend import QuantumBackend, QuantumSimulationLimitError
import grover_algorithm as ga


class QiskitBackend(QuantumBackend):
    """Backend implementation that delegates to the local Grover circuit builders."""

    MAX_QUBITS = 3

    def build_search(self, dataset: Iterable[Any], target: str) -> Any:
        n_items = sum(1 for _ in dataset)
        n_qubits = max(1, math.ceil(math.log2(max(2, n_items))))

        if n_qubits > self.MAX_QUBITS:
            raise QuantumSimulationLimitError(
                f'Número de qubits ({n_qubits}) excede a capacidade do simulador ({self.MAX_QUBITS}).'
            )

        qiskit_target = normalize_bitstring(target, n_qubits=n_qubits)

        if n_qubits == 2:
            return ga.criar_grover_2qubits(qiskit_target)

        try:
            from grover_advanced import grover_3qubits
            return grover_3qubits(qiskit_target)
        except (ImportError, AttributeError) as exc:
            raise RuntimeError('Falha ao carregar o builder de 3 qubits') from exc

    def execute(self, circuit: Any, shots: int = 1024) -> Dict[str, int]:
        counts = ga.executar_grover(circuit, shots=shots)
        return format_bitstring_output(counts, n_qubits=circuit.num_qubits)
