# Handoff: how to deliver work to this repository

This file is for the session that writes the paper and the research notes. That session can read this repository but cannot write to it. A second session, the maintainer, applies each delivery as a pull request, and the owner approves the merge. Read this file before you prepare every delivery; it changes when the process changes.

Repository: https://github.com/Chalolennox/pythagorean-k3-specializations (branch `main`).

## 1. Before you start: read the current state of `main`

Read these on `main`, not from memory of an earlier delivery:

* `paper/REVISION`: the revision number of `paper/paper.md` on `main`.
* `paper/paper.md`: the text on `main`. It can contain text added in the repository, for example sentences accepted from a review. Your working document must contain the same text, or the next delivery will delete it (see section 4).
* The latest commit on `main` (its short hash). Your delivery is built against it, and you name it in the manifest.

## 2. What to deliver

A single zip with the following parts. Leave out what does not apply.

| Part | Path | Notes |
| --- | --- | --- |
| Manifest | `HANDOFF.txt` | Required in every delivery; see section 3. |
| The paper | `paper/paper.md` | The complete exported file, not only a patch. |
| Revision number | `paper/REVISION` | Required whenever `paper.md` changes (section 4). |
| A patch for the paper (optional) | `paper.patch` | A diff against `paper/paper.md` at the base commit. It is used to show the change in review; the complete `paper.md` is what gets applied. |
| New or changed figures | `paper/figures/<name>.png` (and `.pdf`) and the line `<label> <name>.png` in `paper/figures/figures.txt` | See section 5. |
| Code | `code/...` | See section 6. |
| Notes and reviews | `notes/...`, `notes/drafts/...` | Reviews as `notes/REVIEW_<date>_<topic>.md`; reviewed source texts, word for word with a provenance header, in `notes/drafts/`. |
| Edits to `README.md`, `STATE.md` or the CI workflow | Write them out in `HANDOFF.txt` as "file, anchor line, new line", or as a diff. | Do not send scripts that edit files (`apply_doc_edits.py`); the maintainer does not run Python locally and makes the edits by hand from your description. |

**Do not send `paper/paper.pdf`.** CI builds it from `paper/paper.md` on every push to `main` (`.github/workflows/paper-pdf.yml`). A PDF in a delivery is ignored and overwritten.

## 3. The manifest `HANDOFF.txt`

```
base: <short hash of the main commit you built against>
revision: <new revision number, or "unchanged">
paper: changed | unchanged
summary: <one or two sentences: what changed and why>
files:
  paper/paper.md                       changed
  paper/REVISION                       changed (253 -> 254)
  code/verify_something.py             new, add to CI as: python3 code/verify_something.py --quick
  notes/REVIEW_2026-11-15_topic.md     new
readme: <line(s) to add or change in README.md, with the line they follow>
state: <changes to STATE.md, or "none">
missing: <files the delivery refers to but does not contain, or "none">
```

The maintainer compares `base` with the current `main`. If `main` has moved and the delivery touches a file that changed in between, the maintainer stops and asks rather than guessing. In that case, rebuild the delivery on the new `main`.

## 4. Revisions

* `paper/REVISION` is the only place the revision number is stored. `README.md` and `STATE.md` quote it ("revision N"), and `code/check_revision.py` fails CI if they disagree. When you change the number, also give the two edits: the line `paper/paper.md ... (snapshot export, revision N; see paper/REVISION)` in README.md and "revision N of the working document" in STATE.md.
* **The number changes together with the text, and only then.** A delivery that changes `paper/paper.md` raises `paper/REVISION` to the revision of the working document it was exported from. A delivery that does not change `paper.md` leaves the number alone. Never send a new number without the matching `paper.md`.
* **The repository's `paper.md` and your working document must contain the same text.** Text can enter `paper.md` in the repository (for example, accepted sentences from a review, recorded in `notes/drafts/`). Before your next export, copy every such change into your working document; a diff between your previous export and the `paper.md` on `main` shows them. Otherwise your export removes them.
* Record corrections in the paper's own corrections log, as before; the revision number alone does not say what changed.

## 5. Figures

* In `paper.md` a figure is the line `&#91;image: Figure <label>: <caption>\]` on its own paragraph, as your export writes it.
* For every such line, `paper/figures/figures.txt` needs the line `<label> <file>`, for example `B.1 p_plus_t_orbit.png`, and the file must be in `paper/figures/`. The PDF build fails on a figure line without an entry, so a new figure cannot be lost silently.
* Send the PNG (and a PDF version if you have one) and the new `figures.txt` line. Include the script that draws the figure in `code/` if there is one.

## 6. Code

* The maintainer does not run your scripts locally. CI runs them on Ubuntu with Python 3.12 and the packages in `requirements.txt` (currently sympy, numpy, scipy). Name any other dependency in the manifest. A script may use gcc; anything else must be installed by the workflow and must be named.
* A script added to CI must end with exit status 0 when every check passes and 1 otherwise, and must print one line per check. A script that only prints numbers cannot fail and is not added to CI.
* If a full run takes more than about a minute, provide `--quick` and say which flag CI should use.
* Put the expected CI line and a README layout line (`code/<name>.py   <what it checks> (<note it belongs to>)`) in the manifest.
* If the script imports another file of the repository, check that the file is on `main`, or include it in the delivery.

## 7. What the maintainer does with a delivery

1. Unpacks it into an empty scratch folder and compares every file with `main` (new, changed, identical).
2. Checks `base` against `main`; if `paper.patch` is present, checks that it applies.
3. Copies the files, makes the README, STATE and CI edits from the manifest, and opens one pull request. It lists anything missing or inconsistent.
4. CI runs every check, builds the PDF, and attaches the PDF and page previews to the pull request.
5. The owner says "merge"; the maintainer squash-merges and deletes the branch. CI then commits the rebuilt `paper.pdf` to `main`.
