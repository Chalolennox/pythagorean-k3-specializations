#!/usr/bin/env python3
"""Consistency check: the paper revision number lives in paper/REVISION; README.md and STATE.md must quote exactly that number ("revision N").
Git history is not read. Exit 0 = consistent."""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
rev = (root/'paper'/'REVISION').read_text().strip()
ok = rev.isdigit()
if not ok: print('paper/REVISION is not an integer: %r' % rev)
for name in ('README.md', 'STATE.md'):
    nums = re.findall(r'revision (\d+)', (root/name).read_text())
    good = nums and all(n == rev for n in nums)
    print('%-10s revision numbers quoted: %s  %s' % (name, nums, 'ok' if good else 'MISMATCH (paper/REVISION = %s)' % rev)); ok &= bool(good)
sys.exit(0 if ok else 1)
