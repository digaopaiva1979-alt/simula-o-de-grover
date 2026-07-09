IMPLEMENTATION REPORT — normalize_bitstring integration (branch: investigate/endianness)

Summary

Implemented the integration plan approved by the project owner. Changes are
confined to wrapper/utility/documentation layers; the quantum algorithm
implementation (oracle/diffuser/Builders) was not modified.

Files changed (local commits, not pushed)

- utils/bitstring.py
  - Added `format_bitstring_output(counts, n_qubits=None)` which validates
    counts, preserves total shots and returns counts in the representation
    expected by the project's public contract.
  - `normalize_bitstring()` already present and used as-is (contract: input
    MSB-left -> returns internal representation used when building circuits).

- grover_interactive.py
  - Integrated `normalize_bitstring()` at entry point to validate and convert
    user-provided MSB-left bitstrings before calling the unmodified quantum
    builders.
  - Used `format_bitstring_output()` to validate/preserve counts and present
    results in the project's MSB-left convention.
  - Clarified UI by printing both user input (MSB-left) and converted internal
    representation (LSB-right) before circuit construction.

- README.md and exemplos/exemplos_de_execucao.md
  - Documented the MSB-left input contract and noted that wrappers perform a
    single conversion to the Qiskit convention. Added instruction that README
    and examples must be updated in the same PR as implementation.

Testing performed

- Executed existing endianness validation runner:

  ```bash
  python3 tests/run_endianness_tests.py
  ```

  Result: All tests passed locally.

- Ran interactive wrapper smoke runs:

  ```bash
  python3 grover_interactive.py --element 01 --shots 20
  ```

  Verified displayed results are presented in MSB-left and that the target is
  correctly marked.

Notes and rationale

- `format_bitstring_output()` does NOT attempt to auto-detect endianness or
  perform automatic reversal; it validates and preserves counts to match the
  project's observed `get_counts()` behavior and the integration contract.

- The design keeps normalization and formatting confined to boundary layers
  (wrappers, examples, CLI). Quantum builders (`criar_grover_2qubits`,
  `grover_3qubits`) were left untouched.

Next steps (manual actions remaining)

- Open PR from `investigate/endianness` to the default branch when ready.
- Ensure CI for the PR includes `tests/run_endianness_tests.py` and the docs
  checks.
- Request reviewers and follow review checklist from `INTEGRATION_PLAN.md`.

Commits created locally

- feat(utils): add format_bitstring_output to convert get_counts keys to MSB-left and preserve shots
- feat(interactive): integrate normalize_bitstring and format_bitstring_output as entry wrapper
- chore(interactive): show user both MSB-left and converted LSB-right before building circuit
- docs: document MSB-left contract and wrapper conversion in README and examples

Notes: No code was pushed, merged or applied to `main`. All work resides in
`investigate/endianness` local branch.
