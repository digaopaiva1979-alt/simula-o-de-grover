from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable


class QuantumSimulationLimitError(RuntimeError):
    """Raised when the requested quantum search exceeds simulator capacity."""
    pass


class QuantumBackend(ABC):
    """Abstract quantum backend interface."""

    @abstractmethod
    def build_search(self, dataset: Iterable[Any], target: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def execute(self, circuit: Any, shots: int = 1024) -> Dict[str, int]:
        raise NotImplementedError
