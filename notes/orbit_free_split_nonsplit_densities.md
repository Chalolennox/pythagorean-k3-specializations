# Orbit-free split/non-split root densities for Problem H

**Status:** Corollary conditional on the established Galois and square-class calculations in `paper/paper.md`, Appendix F.2–F.7. This note gives the finite character count and an independent numerical check; it does **not** prove a global root-number distribution along an elliptic orbit.

## Setup

Let
[
H(t)=t^6-30t^4-24t^2-1,qquad q(t)=2t(1-t^2).
]
For a prime (p\ge5) away from the finite ramified/degenerate set, put
[
S_p=\#\{r\in\mathbf F_p:H(r)=0,\ (q(r)/p)=+1\},\qquad
N_p=\#\{r\in\mathbf F_p:H(r)=0,\ (q(r)/p)=-1\}.
]
The local multiplicative root-number factor at a discriminant root is (- (q(r)/p)): (S_p) counts sign-changing split roots; (N_p) counts neutral non-split roots. **These are roots available modulo (p), not roots necessarily hit by the orbit.**

## Character-count derivation

The degree-24 splitting field of (H) described in Appendix F.2–F.3 has Frobenius types with 0, 2 and 6 fixed roots in proportions (14/24), (9/24) and (1/24), respectively. The roots come in three opposite pairs (r,-r), and (q(-r)=-q(r)).

The quadratic character of (-1) is independent of the degree-24 splitting field, by the field and square-class computations in Appendix F.5 (which adjoins (sqrt{-1})). Thus, conditional on a nonempty root set, half the Frobenius elements have ((-1/p)=-1), making each fixed opposite pair contribute one split and one non-split root.

When ((-1/p)=+1), the characters of (q(r)) are equal within each fixed opposite pair. For two fixed roots there is one pair and its character is equidistributed. For six fixed roots there are three pairs; the three signs are jointly uniform in ({\pm1\}^3) after averaging over the independent quadratic characters of the extension in F.5. In particular, for six fixed roots, the conditional probabilities of ((S_p,N_p)=(6,0),(4,2),(2,4),(0,6)) are (1/8,3/8,3/8,1/8) **within the ((-1/p)=+1) half**. The other half yields ((3,3)).

Consequently, by Chebotarev, the only positive-density joint configurations are:

| (S_p) | (N_p) | Natural density | Count for (5\le p\le100000) |
|---:|---:|---:|---:|
| 0 | 0 | (7/12) | 5626 |
| 1 | 1 | (3/16) | 1787 |
| 2 | 0 | (3/32) | 931 |
| 0 | 2 | (3/32) | 857 |
| 3 | 3 | (1/48) | 206 |
| 4 | 2 | (1/128) | 67 |
| 2 | 4 | (1/128) | 63 |
| 6 | 0 | (1/384) | 24 |
| 0 | 6 | (1/384) | 29 |

The nine rational densities sum to one. All other configurations have density zero (and are excluded away from the exceptional set under the stated Galois description).

## Exact consequences

[
\begin{aligned}
\delta(S_p>0)&=\delta(N_p>0)=\frac{41}{128},\\
\delta(S_p>0,\ N_p>0)&=\frac{43}{192},\\
\delta(S_p=N_p)&=\frac{19}{24},\\
\mathbb E[S_p]&=\mathbb E[N_p]=\frac12,\\
\mathbb E[N_p-S_p]&=0.
\end{aligned}
]

The observed sample of 9590 primes (5\le p\le100000) gave total split roots 4805 and total non-split roots 4679, so empirical means (0.50104275) and (0.48790407), and empirical mean signed difference (-126/9590\approx-0.01313869). The observed equality frequency was (7619/9590\approx0.79447), compared with (19/24\approx0.79167). These are finite-sample checks, not proofs.

## Scope and limitations

This is a **prime-level, orbit-free** Chebotarev count. The density (175/1024) in Appendix F.3 concerns a *different* admissibility condition and must not be identified with the (41/128) density here. The subgroup-accessibility obstruction of Appendix F.4 remains: a root of (H) modulo (p) need not equal (1-x(nP+T)) for any (n). Even exact equality of split/non-split mean root counts therefore does **not** establish cancellation, parity equidistribution, or infinitely many positive global root numbers along the rational orbit.

**Review point:** The nine-class table is a corollary of the square-class rank and independence statements of F.5; a reviewer should check the asserted joint uniformity of the three (q(r)) characters on the six-root Frobenius class before promoting this note to an unconditional theorem in the main paper.
