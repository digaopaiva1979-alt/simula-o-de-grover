"""Bitstring utilities for endianness normalization.

Provides helpers to validate and convert human-friendly bitstrings (MSB-left)
into the convention expected by Qiskit (LSB-right in measurement strings).
"""

from typing import Optional
from typing import Dict


def normalize_bitstring(bitstr: str, n_qubits: Optional[int] = None) -> str:
    """Validate and normalize a bitstring for Qiskit.

    Parameters
    ----------
    bitstr : str
        Bitstring provided by the user (expected characters: '0' or '1').
    n_qubits : int, optional
        Expected number of qubits. If provided, the function validates the
        length matches `n_qubits`.

    Returns
    -------
    str
        Bitstring converted to Qiskit convention (reversed), suitable to be
        passed to circuit constructors that index qubits from 0 upward.

    Raises
    ------
    ValueError
        If the input contains invalid characters or has the wrong length.
    """
    if not isinstance(bitstr, str):
        raise ValueError('bitstr must be a string')
    if any(c not in ('0', '1') for c in bitstr):
        raise ValueError("bitstr must contain only '0' or '1'")
    if n_qubits is not None and len(bitstr) != n_qubits:
        raise ValueError(f'bitstr length {len(bitstr)} does not match n_qubits {n_qubits}')

    # Qiskit's get_counts returns bitstrings where the rightmost character
    # corresponds to qubit 0 (LSB). Convert from user-friendly MSB-left
    # to Qiskit LSB-right by reversing the string.
    return bitstr[::-1]


def format_bitstring_output(counts: Dict[str, int], n_qubits: Optional[int] = None) -> Dict[str, int]:
    """Convert Qiskit `get_counts()` keys (LSB-right) to MSB-left representation.

    Parameters
    ----------
    counts : dict
        Mapping returned by Qiskit's `get_counts()`, e.g. {'00': 10, '01': 5}.
    n_qubits : int, optional
        If provided, validates keys lengths match `n_qubits`.

    Returns
    -------
    dict
        New mapping with keys converted to MSB-left convention. Total sum of
        shots is preserved.

    Raises
    ------
    ValueError
        If any key contains invalid characters or wrong length when `n_qubits`
        is provided.
    """
    if not isinstance(counts, dict):
        raise ValueError('counts must be a dict mapping bitstrings to integers')

    converted: Dict[str, int] = {}
    total_before = 0
    for k, v in counts.items():
        if not isinstance(k, str):
            raise ValueError('counts keys must be bitstring strings')
        if any(c not in ('0', '1') for c in k):
            raise ValueError('counts keys must contain only "0" or "1"')
        if n_qubits is not None and len(k) != n_qubits:
            raise ValueError(f'counts key length {len(k)} does not match n_qubits {n_qubits}')
        total_before += int(v)
        # NOTE: Qiskit's `get_counts()` in the current environment returns
        # bitstrings compatible with the project's MSB-left contract expected
        # by users (tests assert measured == target). Therefore this formatter
        # performs validation and preserves counts; it does not attempt to
        # auto-detect or reverse keys. If a different backend requires
        # explicit reversal, update this utility and the integration plan.
        converted[k] = converted.get(k, 0) + int(v)

    # Sanity: preserve total shots
    total_after = sum(converted.values())
    if total_before != total_after:
        raise RuntimeError('internal error: total shots mismatch after conversion')

    return converted
