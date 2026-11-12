#!/usr/bin/env python3
"""Figure B.1 of the paper: the orbit of S = P + T on the auxiliary curve C : y^2 = x^3 - 2x^2 + 2x, drawn on the unit circle.
Point n is (A_n, B_n) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)) with t = t(nS) = 1 - x(nS), n = 1..30; since nS = nP + nT, t(nS) = t'_n = t(nP + T) for odd n and t_n = t(nP) for even n.
Because t(Q) = t(-Q), the translation by S is a two-valued correspondence on t: t(Q) -> {t(Q + S), t(Q - S)}.  On the orbit these are the neighbours n+1 and n-1.
Solid arrows: n -> n+1 (forward, translation by S).  Dashed arcs: n -> n-1 (the other value of the correspondence).
All coordinates come from exact rational arithmetic; the script asserts the six t-values listed in Appendix B.   Needs matplotlib.
Usage: python3 code/figure_p_plus_t_orbit.py [output directory, default paper/figures]   writes p_plus_t_orbit.png (220 dpi) and p_plus_t_orbit.pdf
       python3 code/figure_p_plus_t_orbit.py --check   exact computation and assertions only (no matplotlib), for CI"""
import sys, os, math
from fractions import Fraction as Fr

# --- exact orbit on y^2 = x^3 - 2x^2 + 2x
a2, a4 = -2, 2
def add(P, Q):
    if P is None: return Q
    if Q is None: return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and y1 == -y2: return None
    lam = (3*x1*x1 + 2*a2*x1 + a4)/(2*y1) if P == Q else (y2 - y1)/(x2 - x1)
    x3 = lam*lam - a2 - x1 - x2
    return (x3, lam*(x1 - x3) - y1)
P0, T0 = (Fr(1), Fr(1)), (Fr(0), Fr(0)); S = add(P0, T0)
assert S == (2, -2)
N = 30; ts = []; Q = None
for n in range(1, N + 1):
    Q = add(Q, S); ts.append(1 - Q[0])
# t-values of the first six points as listed in Appendix B (t(P+T), t(2P), t(3P+T), t(4P), t(5P+T), t(6P))
assert ts[:6] == [Fr(-1), Fr(3, 4), Fr(31, 49), Fr(-561, 400), Fr(-69409, 529), Fr(-2047837, 2965284)]
AB = [(float((1 - t*t)/(1 + t*t)), float(2*t/(1 + t*t))) for t in ts]
assert all(abs(A*A + B*B - 1) < 1e-12 for A, B in AB)

if '--check' in sys.argv:
    print('exact orbit of P + T, n = 1..%d: all points on the unit circle, t_1..t_6 agree with Appendix B' % N); sys.exit(0)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D

# --- label angles: push labels apart along the circle (minimum gap), keeping their order, cutting the circle at its largest gap
theta = sorted(((math.atan2(B, A) % (2*math.pi), n) for n, (A, B) in enumerate(AB, 1)))
gaps = [(theta[(i + 1) % N][0] - theta[i][0]) % (2*math.pi) for i in range(N)]
cut = (max(range(N), key=lambda i: gaps[i]) + 1) % N
order = theta[cut:] + theta[:cut]; base = order[0][0]
ang = [((a - base) % (2*math.pi), n) for a, n in order]; pos = [a for a, n in ang]; gmin = math.radians(3.6)
for _ in range(4000):
    moved = False
    for i in range(N - 1):
        d = pos[i + 1] - pos[i]
        if d < gmin - 1e-9: pos[i] -= (gmin - d)/2; pos[i + 1] += (gmin - d)/2; moved = True
    if not moved: break
labelpos = {n: (math.cos(base + p), math.sin(base + p)) for (a, n), p in zip(ang, pos)}

fig, ax = plt.subplots(figsize=(7.4, 7.4))
th = [i*math.pi/180 for i in range(361)]
ax.plot([math.cos(x) for x in th], [math.sin(x) for x in th], color='black', lw=1.0, zorder=1)
ax.axhline(0, color='0.85', lw=0.8, zorder=0); ax.axvline(0, color='0.85', lw=0.8, zorder=0)
RAD = 0.12
for n in range(1, N):            # forward arrow n -> n+1 and the other branch (n+1 -> n), both drawn with the same curvature so that they are mirror images
    p, q = AB[n - 1], AB[n]
    ax.add_patch(FancyArrowPatch(q, p, connectionstyle='arc3,rad=%g' % RAD, arrowstyle='-', color='0.55', lw=0.7, ls=(0, (3, 3)), alpha=0.8, zorder=2))
for n in range(1, N):
    p, q = AB[n - 1], AB[n]
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle='arc3,rad=%g' % RAD, arrowstyle='-|>', mutation_scale=6, color='#4a7be0', lw=0.9, alpha=0.8, shrinkA=2.5, shrinkB=2.5, zorder=3))
ax.scatter([A for A, B in AB], [B for A, B in AB], s=16, color='black', zorder=5)
for n, (lx, ly) in labelpos.items():
    A, B = AB[n - 1]; R1 = 1.095
    ax.plot([A, lx*1.045], [B, ly*1.045], color='0.5', lw=0.4, zorder=1)
    ax.text(lx*R1, ly*R1, str(n), fontsize=7.5, color='#10107a', ha='center', va='center', zorder=6)
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_aspect('equal'); ax.set_xlabel('A'); ax.set_ylabel('B')
ax.set_xticks([-1, -0.5, 0, 0.5, 1]); ax.set_yticks([-1, -0.5, 0, 0.5, 1]); ax.tick_params(labelsize=8)
for s in ax.spines.values(): s.set_visible(False)
ax.legend(handles=[Line2D([], [], marker='o', ls='', color='black', ms=4, label='orbit point n = 1, …, 30'),
                   Line2D([], [], color='#4a7be0', lw=1.2, label='forward: n → n + 1 (translation by P + T)'),
                   Line2D([], [], color='0.55', lw=1.0, ls=(0, (3, 3)), label='other branch: n → n − 1')], loc='upper right', fontsize=7.5, frameon=True, framealpha=0.95)
args = [a for a in sys.argv[1:] if not a.startswith('--')]
out = args[0] if args else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'paper', 'figures')
os.makedirs(out, exist_ok=True); fig.tight_layout()
fig.savefig(os.path.join(out, 'p_plus_t_orbit.png'), dpi=220); fig.savefig(os.path.join(out, 'p_plus_t_orbit.pdf'))
print('wrote', os.path.join(out, 'p_plus_t_orbit.png'), 'and .pdf;  t_1..t_6 =', [str(t) for t in ts[:6]], ';  min label gap %.1f degrees' % math.degrees(gmin))
