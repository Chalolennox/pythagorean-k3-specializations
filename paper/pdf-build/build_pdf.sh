#!/usr/bin/env bash
# Build paper/paper.pdf from paper/paper.md (run from anywhere; used by .github/workflows/paper-pdf.yml).
#   1. replace the figure placeholders "&#91;image: Figure <label>: ...\]" by the files listed in paper/figures/figures.txt
#      (fails if a placeholder has no entry, so a new figure cannot be dropped silently);
#   2. check that every character of paper.md is covered by an installed font (fails otherwise, so no blank boxes in the PDF);
#   3. pandoc: markdown -> standalone HTML;  4. WeasyPrint: HTML + paper/pdf-build/paper.css -> paper/paper.pdf.
# Needs: pandoc, weasyprint, fontconfig (fc-list), perl.
set -euo pipefail
export LC_ALL=C.UTF-8
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="$ROOT/paper/paper.md"; OUT="$ROOT/paper/paper.pdf"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
cp "$SRC" "$TMP/paper.md"

# 1. figures
while read -r label file; do
  [[ -z "$label" || "$label" == \#* ]] && continue
  [[ -f "$ROOT/paper/figures/$file" ]] || { echo "figures.txt: paper/figures/$file not found" >&2; exit 1; }
  LABEL="$label" FILE="paper/figures/$file" perl -CSD -i -pe '
    BEGIN { $l = quotemeta($ENV{LABEL}); $f = $ENV{FILE} }
    s{^&#91;image: (Figure $l\b.*?)\\?\]\s*$}{![$1]($f)\n};' "$TMP/paper.md"
done < "$ROOT/paper/figures/figures.txt"
if grep -n '^&#91;image:' "$TMP/paper.md"; then
  echo "unmapped figure placeholder(s) above: add them to paper/figures/figures.txt" >&2; exit 1
fi

# 2. glyph coverage
missing=0
n=0
while IFS= read -r hex; do
  [[ -z "$hex" ]] && continue; n=$((n + 1))
  if [[ -z "$(fc-list ":charset=$hex" family | head -n 1)" ]]; then echo "no installed font has U+$hex" >&2; missing=1; fi
done < <(perl -CSD -ne 'printf "%x\n", ord for /[^\x00-\x7F]/g' "$SRC" | sort -u)
[[ $missing == 0 ]] || exit 1
echo "glyph check: all $n distinct non-ASCII characters of paper.md are covered by installed fonts"

# 3.-4. pandoc and WeasyPrint (superscript/subscript/TeX extensions off: the export writes math as plain Unicode, and ^ or ~ in it must stay literal)
pandoc -f markdown-implicit_figures-superscript-subscript-tex_math_dollars-raw_tex -t html5 -s -V document-css=false \
  --metadata pagetitle="Pythagorean Specializations of an Elliptic K3 Surface" -o "$TMP/paper.html" "$TMP/paper.md"
weasyprint --base-url "$ROOT/" -s "$ROOT/paper/pdf-build/paper.css" "$TMP/paper.html" "$OUT"
echo "built $OUT ($(wc -c < "$OUT") bytes)"
