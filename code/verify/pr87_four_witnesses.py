#!/usr/bin/env python3
"""Independent check of the four residue witnesses in PR #87 (notes/orbit_free_split_nonsplit_densities.md).

Written by Claude (a language model), independent of the PR author's scripts
(none is in the repository). No human has checked it. Evidence from Claude, not a
Certified result.

Checks (stdlib only, exact integer arithmetic):
  1. For each witness (p, triple): all six +-entries are distinct roots of
     H(t) = t^6 - 30 t^4 - 24 t^2 - 1 mod p, the product of the triple is 1 mod p,
     p does not divide the discriminant of H (H squarefree mod p, p>=5), and the
     Legendre-symbol bits of (-1, q(a1), q(a2), q(a3)), q(t) = 2t(1-t^2), equal the
     bits stated in the note.
  2. The four bit-vectors have rank 4 over F2.
  3. Extra: for all primes 5<=p<=1000 with six roots mod p, the span of the bit
     vectors over all ordered triples with product 1 (one per labelled triple)
     has rank 4 (rank taken over the union of all such primes).
Does NOT check: that Gal(H) has order 24 / the even signed permutation group
(Appendix F.2), the Kummer/Chebotarev argument, the density table, or the 9590-prime
Magma counts.
Runtime: well under 10 seconds.
"""
import itertools

def H(t, p): return (t**6 - 30*t**4 - 24*t**2 - 1) % p
def q(t, p): return (2*t*(1 - t*t)) % p
def bit(v, p):
    v %= p
    assert v != 0
    return 0 if pow(v, (p-1)//2, p) == 1 else 1
def rank(vs):
    basis = []
    for v in vs:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis)
def vec(bits): return int(''.join(map(str, bits)), 2)
def bits_of(tr, p): return (bit(-1, p),) + tuple(bit(q(x, p), p) for x in tr)

W = [(83, (18, 32, 33), (1,0,1,0)), (83, (18, 33, 32), (1,0,0,1)),
     (83, (32, 18, 33), (1,1,0,0)), (307, (39, 132, 147), (1,1,0,1))]
rows = []
for p, tr, stated in W:
    roots = [r for r in range(p) if H(r, p) == 0]
    signed = [x % p for x in tr] + [(-x) % p for x in tr]
    # squarefree mod p: all 6 roots distinct (degree 6, 6 roots found)
    ok = (len(roots) == 6 and all(H(x, p) == 0 for x in tr) and len(set(signed)) == 6
          and (tr[0]*tr[1]*tr[2]) % p == 1)
    got = bits_of(tr, p)
    print(p, tr, "valid:", ok, "bits:", got, "stated:", stated, "match:", got == stated)
    assert ok and got == stated
    rows.append(vec(got))
print("rank of the four rows over F2:", rank(rows))
assert rank(rows) == 4
# extra scan
def primes(n):
    s = bytearray([1])*(n+1); s[0]=s[1]=0
    for i in range(2, int(n**.5)+1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]
total = 0
for p in primes(1000):
    if p < 5: continue
    roots = [r for r in range(p) if H(r, p) == 0]
    if len(roots) != 6: continue
    pairs = sorted({min(r, p-r) for r in roots})
    vs = []
    for perm in itertools.permutations(pairs):
        for s in itertools.product((1, -1), repeat=3):
            tr = tuple((s[i]*perm[i]) % p for i in range(3))
            if (tr[0]*tr[1]*tr[2]) % p == 1:
                vs.append(vec(bits_of(tr, p)))
    total += 1
print("primes <=1000 with six roots mod p:", total)
allv = []
for p in primes(1000):
    if p < 5: continue
    roots = [r for r in range(p) if H(r, p) == 0]
    if len(roots) != 6: continue
    pairs = sorted({min(r, p-r) for r in roots})
    for perm in itertools.permutations(pairs):
        for s in itertools.product((1, -1), repeat=3):
            tr = tuple((s[i]*perm[i]) % p for i in range(3))
            if (tr[0]*tr[1]*tr[2]) % p == 1:
                allv.append(vec(bits_of(tr, p)))
print("rank of all bit vectors over all such triples, p<=1000:", rank(allv))
