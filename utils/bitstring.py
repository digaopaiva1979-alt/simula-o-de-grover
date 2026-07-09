"""Bitstring utilities for endianness normalization.

Provides helpers to validate and convert human-friendly bitstrings (MSB-left)
into the convention expected by Qiskit (LSB-right in measurement strings).
"""

from typing import Optional


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
