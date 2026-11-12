#!/usr/bin/env python3
"""Consistency check: Problem H is the SIGN statement  W(E_{t_n}) = +1 for infinitely many n  (t_n = 1 - x(nP)), everywhere.
It is not the rank statement; rank >= 2 follows from it only through paper section 6 (2-parity theorem, and finiteness of Sha[2^oo] for the last step).
Checks (README.md, STATE.md, paper/paper.md):  (1) the canonical statement occurs in each file;  (2) none of the old phrasings that called Problem H a rank statement occurs;
(3) the paper has its definition paragraph and its Appendix B states both sequences.  Usage: python3 code/check_problem_h_definition.py [repo root]   Exit 0 = consistent.  Stdlib only."""
import re, sys, os
root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
def norm(s): return re.sub(r'\s+', ' ', s.replace('\\', ''))          # drop markdown escapes, collapse whitespace
files = {f: norm(open(os.path.join(root, f), encoding='utf-8').read()) for f in ('README.md', 'STATE.md', 'paper/paper.md')}
bad = []
canon = 'W(E_{t_n}) = +1 for infinitely many n'
for f, t in files.items():
    if canon not in t and 'infinitely many n with W(E_{t_n}) = +1' not in t and 'root number of E_{t_n} is +1 for infinitely many n' not in t: bad.append('%s: the canonical statement of Problem H is missing' % f)
old = [r'rank ≥ 2 \(Problem H', r'only obstacle to infinitely many members of rank', r'one open problem: \*\*are there infinitely many members of rank', r'Infinitely many members of rank ≥ 2 \(Problem H\)',
       r'rank ≥ 2 \| Open \| Problem H', r'Infinitely many t with rank ≥ 2 \(Problem H']
for f, t in files.items():
    for pat in old:
        for m in re.finditer(pat, t): bad.append('%s: old phrasing "%s"' % (f, t[max(0, m.start() - 30):m.end() + 30]))
p = files['paper/paper.md']
for need, why in (('Throughout, Problem H is the statement about the sign', 'definition paragraph in "Results at a glance"'), ('Problem H along nP + T', 'Appendix B names the second sequence'),
                  ('Problem H implies H_2', 'link between Problem H and the hypothesis H_c of section 6')):
    if need not in p: bad.append('paper/paper.md: missing %s' % why)
for b in bad: print('FAIL', b)
print('Problem H is defined consistently in README.md, STATE.md and paper/paper.md' if not bad else '%d inconsistencies' % len(bad)); sys.exit(1 if bad else 0)
