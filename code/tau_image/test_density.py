"""Validation of density.py against Table 1 of Liang-Rouse (rows 1-17: the subgroups Gamma_0^o(2) and H_2 * M_d, defined in Section 4 of the paper)."""
import sys, itertools, time
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from density import density, gl2_elements
r = 3; q = 8
GL = gl2_elements(q)
# the group Gamma_0^o(2): c even, (e, f) arbitrary
def elements(pred):
    return [(e, f, a, b, c, d) for (a, b, c, d) in GL if c % 2 == 0 for e in range(q) for f in range(q) if pred(e, f, a, b, c, d)]
inH2   = lambda e, f, a, b, c, d: e % 2 == 0
inMm1  = lambda e, f, a, b, c, d: ((a*d - b*c) % 4) == 1                  # M_{-1}: det = 1 mod 4
inM2   = lambda e, f, a, b, c, d: ((a*d - b*c) % 8) in (1, 7)            # M_2   : det = +-1 mod 8
inMb   = lambda e, f, a, b, c, d: c % 4 == 0                              # M_b   : c = 0 mod 4
inMD   = lambda e, f, a, b, c, d: b % 2 == 0                              # M_{a^2-4b}: b = 0 mod 2
def star(*preds):                                                          # M_{d1 d2 ...} = M_{d1} * M_{d2} * ... : g in it iff an even number of the preds fail
    return lambda *g: sum(0 if p(*g) else 1 for p in preds) % 2 == 0
def H2star(*preds):
    s = star(*preds); return lambda *g: inH2(*g) == s(*g)
# row -> (generators used in d, expected density)
rows = {1: (None, Fr(5, 21)), 2: ('H2', Fr(10, 21)),
        3: ((-1, 2, 'b', 'D'), Fr(5123, 21504)), 4: ((-1, 2, 'b'), Fr(5123, 21504)), 5: ((2, 'b', 'D'), Fr(5123, 21504)), 6: ((2, 'b'), Fr(5123, 21504)),
        7: ((-1, 'b', 'D'), Fr(83, 336)), 8: ((-1, 'b'), Fr(83, 336)), 9: (('b', 'D'), Fr(13, 42)), 10: (('b',), Fr(1, 7)),
        11: ((-1, 2, 'D'), Fr(5123, 21504)), 12: ((-1, 2), Fr(5123, 21504)), 13: ((2, 'D'), Fr(5123, 21504)), 14: ((2,), Fr(5123, 21504)),
        15: ((-1, 'D'), Fr(83, 336)), 16: ((-1,), Fr(83, 336)), 17: (('D',), Fr(1, 7))}
gen = {-1: inMm1, 2: inM2, 'b': inMb, 'D': inMD}
ok = True
for row, (spec, expected) in rows.items():
    t0 = time.time()
    if spec is None: G = elements(lambda *g: True)
    elif spec == 'H2': G = elements(inH2)
    else: G = elements(H2star(*[gen[s] for s in spec]))
    val = density(G, r) if row > 2 else density(G, r)
    good = (val == expected); ok &= good
    print("row %2d: |G| = %6d  density %-12s expected %-12s %s  (%.1fs)" % (row, len(G), val, expected, "OK" if good else "MISMATCH", time.time() - t0), flush=True)
print("ALL ROWS 1-17 MATCH" if ok else "SOME MISMATCH")
