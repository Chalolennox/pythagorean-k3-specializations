# Torsion and P-division tower disjointness
Proof given, human review pending.

Let J:y²=x³−2x²+2x, P=(1,1), K the splitting field of the twelve geometric points with h(x)=0 and y²=f(x), T∞ the 2-power torsion field, and E∞=T∞(2^(-n)P : n>=1).

Theorem: K ∩ E∞ = Q, hence K ∩ T∞ = Q. The P-translation index 32 is unchanged over KT∞.

Proof: E∞/Q is Galois pro-2: the mod-2 torsion image has order 2, higher torsion kernels and affine translation kernels are 2-groups. At each odd prime J has good reduction (discriminant −256), and P extends to a section of the abelian scheme over the local integers by properness. Multiplication by 2^n is finite étale there, so both its torsion and the fiber above P are unramified. Thus E∞ is unramified outside 2. A nontrivial finite Galois intersection with K would have a nontrivial finite 2-group as Galois group, hence a quadratic subfield, necessarily Q(sqrt(-1)), Q(sqrt(2)) or Q(sqrt(-2)). The two primes below split completely in K: h has six distinct roots and f is a nonzero square at each. Hensel lifting gives all twelve points over Q_p, proving complete splitting. Their quadratic characters exclude all three fields. Therefore K and E∞ are linearly disjoint. Restriction identifies Gal(K E∞/K T∞) with Gal(E∞/T∞), preserving the P-index.

Replay: code/magma/pr92_torsion_intersection.m (compact version of owner-run script; not independently executed).

## Owner output (27 November 2026)
```
============================================
EXACT TORSION INTERSECTION
============================================
Curve discriminant: -256
Ramification support: {2}
--------------------------------------------
Prime: 2621
Verified point: 65 2170
Verified point: 271 1381
Verified point: 1072 1994
Verified point: 1551 1678
Verified point: 2352 2024
Verified point: 2558 555
Six distinct x-coordinates: PASS
Twelve rational geometric points: PASS
Complete splitting in K: PASS
Prime modulo 8: 5
Quadratic characters: [ 1, -1, -1 ]
--------------------------------------------
Prime: 93491
Verified point: 6819 64492
Verified point: 14743 62466
Verified point: 42222 6366
Verified point: 51271 59157
Verified point: 78750 13291
Verified point: 86674 78189
Six distinct x-coordinates: PASS
Twelve rational geometric points: PASS
Complete splitting in K: PASS
Prime modulo 8: 3
Quadratic characters: [ -1, -1, 1 ]
--------------------------------------------
Quadratic class -1 excluded: true
Quadratic class 2 excluded: true
Quadratic class -2 excluded: true
============================================
ALL QUADRATIC SUBFIELDS EXCLUDED
TORSION INTERSECTION CERTIFICATE: PASS
K intersect T_infty = Q
============================================

# 875ms · Magma V2.30-1 | 0.09s | 32.09MB | seed 2499168731
```

This does not prove independence of P from U division towers, nor saturation at 2. No claim on Problem H.
