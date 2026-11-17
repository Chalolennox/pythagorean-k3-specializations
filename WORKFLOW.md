# Workflow: how changes enter this repository

Since 17 November 2026 changes are made as pull requests by the session that writes the paper and the notes. The earlier process (a zip with a manifest `HANDOFF.txt`, applied by hand by a second session) is obsolete, and so is the file `HANDOFF.md` that described it.

## 1. The process

1. Branch from the current `main` (read its latest commit and `paper/REVISION` first). Name the branch `<topic>-<date>`. Never push to `main`; CI commits the rebuilt `paper/paper.pdf` to `main` and nothing else does.
2. Make the change in the branch: paper text, notes, code, figures, and the README, STATE and CI edits that go with them, as ordinary commits. Do not add `paper/paper.pdf` to a branch (CI builds it from `paper/paper.md` with `.github/workflows/paper-pdf.yml`).
3. Open a pull request against `main`. The description says what changed and why, what status label each new claim has, what was checked and what was not (which CI scripts were run, which were not). Commits and pull requests made by a language model carry the attribution lines it is given.
4. CI (`.github/workflows/validate.yml`) runs every check and builds the PDF. A pull request is merged only when CI is green and the owner has said "merge"; the merge is a squash merge and the branch is deleted.
5. If `main` moves while a pull request is open, rebase the branch onto it; do not merge over a conflict.

## 2. Revision number and the working document

* `paper/REVISION` is the only place the revision number is stored. `README.md` and `STATE.md` quote it ("revision N"), and `code/check_revision.py` fails CI if they disagree. When the number changes, change the line `paper/paper.md ... (snapshot export, revision N; see paper/REVISION)` in `README.md` and "revision N of the working document" in `STATE.md` in the same pull request.
* **The number changes together with the text, and only then.** A pull request that changes `paper/paper.md` sets `paper/REVISION` to the revision of the working document it was exported from. A pull request that does not change `paper.md` leaves the number alone. Never change the number without the matching `paper.md`.
* **The repository's `paper.md` and the working document must contain the same text.** Text can enter `paper.md` in the repository (for example sentences accepted from a review, recorded in `notes/drafts/`). Before the next export, diff the previous export against `paper.md` on `main` and copy every such change into the working document; otherwise the export removes it.
* Record corrections in the paper's own corrections log; the revision number alone does not say what changed.

## 3. Notes, reviews and sources

* Reviews and notes: `notes/REVIEW_<date>_<topic>.md`, `notes/<topic>.md`.
* A reviewed source text (a dossier, a draft written by someone else) goes into `notes/drafts/` word for word: a provenance header, then the unmodified text (see the existing files for the form; a Magma or other script gets the same header in its own comment syntax).
* Every claim carries one of the paper's labels (Proved, Certified, Observed, Conditional, Open) and, when it was derived with a language model, says that no human has checked it.

## 4. Figures

* In `paper.md` a figure is the line `&#91;image: Figure <label>: <caption>\]` on its own paragraph, as the export writes it.
* For every such line, `paper/figures/figures.txt` needs the line `<label> <file>` (for example `B.1 p_plus_t_orbit.png`) and the file must be in `paper/figures/`. The PDF build fails on a figure line without an entry. Add the PNG (and a PDF version if there is one) and, if a script draws the figure, the script in `code/`.

## 5. Code

* CI runs on Ubuntu with Python 3.12 and the packages in `requirements.txt` (currently sympy, numpy, scipy). A script may use gcc; anything else must be installed by the workflow.
* A script added to CI ends with exit status 0 when every check passes and 1 otherwise, and prints one line per check. A script that only prints numbers cannot fail and is not added to CI.
* If a full run takes more than about a minute, provide `--quick` and use it in CI.
* Add a layout line to the README (`code/<name>.py   <what it checks> (<note it belongs to>)`) and the `- run:` line to `.github/workflows/validate.yml`.
* A script that imports another file of the repository must find that file on `main` or in the same pull request.
