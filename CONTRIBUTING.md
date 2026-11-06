# Contributing

Thank you for looking at this. The project is a research record, and its value depends on honest labels, so the most useful contributions are **independent checks, corrections and counter-examples**.

## The claims policy

Every statement in the paper carries one label:

| Label | Meaning |
| --- | --- |
| Proved | a complete proof, read by a human |
| Certified | an exact computation that was independently re-checked |
| Observed | a finite computation, with its limits stated |
| Conditional | depends on a hypothesis that is named |
| Open | not known |

Please do not change a label without evidence in the same pull request. A downgrade needs only a reason; an upgrade needs a proof or an independent computation that can be rerun.

## How to report a problem

Open an issue using one of the templates: **possible error** (something in the paper, code or data looks wrong) or **claim to verify** (you have checked, or want to check, a particular statement).

## Pull requests

1. Run `python3 code/validate.py` and `python3 code/verify_factorizations.py`; both must pass.
2. Put new computations in a script with its inputs and its output, and say how long it takes.
3. If you correct an error, add a row to `ERRATA.md`.
4. **Say whether any text or code in the pull request was written or checked with a language model**, and which. This applies to everything, including small changes.
5. Contributions are accepted under the MIT license of this repository.

## Style

Short sentences; a statement and its status together; the hypothesis before the result; numbers with their units and sources. Do not cite a reference you have not looked up.
