# Orbit-free split/non-split root densities for Problem H

**Status:** Proof given, using the splitting-field description in Appendix E/F.2 and the direct four-class certificate below. It does **not** prove a global root-number distribution along an elliptic orbit.

## Setup

Let
\[
H(t)=t^6-30t^4-24t^2-1,\qquad q(t)=2t(1-t^2).
\]
For primes \(p\ge5\) away from the finite exceptional set, put
\[
S_p=\#\{r\in\mathbf F_p:H(r)=0,\ (q(r)/p)=+1\},\qquad
N_p=\#\{r\in\mathbf F_p:H(r)=0,\ (q(r)/p)=-1\}.
\]
At a simple discriminant root, the local multiplicative root-number factor is \(-(q(r)/p)\): \(S_p\) counts sign-changing split roots and \(N_p\) counts neutral non-split roots. **These count available roots modulo \(p\), not necessarily roots hit by the orbit.**

## Chebotarev calculation

The degree-24 splitting field of \(H\) described in Appendix F.2–F.3 has Frobenius classes with 0, 2 and 6 fixed roots in proportions \(14/24\), \(9/24\) and \(1/24\). Roots come in three opposite pairs \(r,-r\), with \(q(-r)=-q(r)\).

By the direct four-class certificate below, the quadratic character \((-1/p)\) is independent of the splitting field. For \((-1/p)=-1\), each fixed opposite pair contributes one split and one non-split root. For \((-1/p)=+1\), the two roots of each fixed pair have the same character.

On the two-root class, that pair character is equidistributed. On the six-root class, the three pair characters are jointly uniform in \(\{\pm1\}^3\), conditional on \((-1/p)=+1\). The direct certificate below proves the required conditional joint uniformity, independently of the rank-10 calculation.

Thus the joint natural densities are:

| \(S_p\) | \(N_p\) | Natural density | Reported observed primes \(5\le p\le100000\) |
|---:|---:|---:|---:|
| 0 | 0 | \(7/12\) | 5626 |
| 1 | 1 | \(3/16\) | 1787 |
| 2 | 0 | \(3/32\) | 931 |
| 0 | 2 | \(3/32\) | 857 |
| 3 | 3 | \(1/48\) | 206 |
| 4 | 2 | \(1/128\) | 67 |
| 2 | 4 | \(1/128\) | 63 |
| 6 | 0 | \(1/384\) | 24 |
| 0 | 6 | \(1/384\) | 29 |

These nine densities sum to one; all other pairs have density zero away from exceptional primes.

## Exact consequences

\[
\begin{aligned}
\delta(S_p>0)&=\delta(N_p>0)=\frac{41}{128},\\
\delta(S_p>0,\ N_p>0)&=\frac{43}{192},\\
\delta(S_p=N_p)&=\frac{19}{24},\\
\mathbb E[S_p]&=\mathbb E[N_p]=\frac12,\\
\mathbb E[N_p-S_p]&=0.
\end{aligned}
\]

In the sample of 9590 primes \(5\le p\le100000\), total split roots were 4805 and non-split roots 4679, giving empirical means \(0.50104275\) and \(0.48790407\). The signed difference was \(-126/9590\approx-0.01313869\). Equal counts occurred at 7619 primes, versus predicted frequency \(19/24\).

## Limitations

The \(175/1024\) density in F.3 concerns a different *admissibility* condition; it is not the \(41/128\) density here. The subgroup-accessibility obstruction in F.4 remains: a root of \(H\) modulo \(p\) need not be attained by \(1-x(nP+T)\). Equal average split/non-split root counts do **not** establish cancellation or parity equidistribution of global root numbers along the rational orbit.

## Direct four-class independence certificate (24 November 2026)

**Proof given**, using the degree-24 splitting-field description of Appendix E/F.2, but not the rank-10 computation of F.5. Written with ChatGPT assistance; no independent human proof review. The finite residue witnesses below were computed with exact Python modular arithmetic.

Choose roots \(a_1,a_2,a_3\) from distinct opposite pairs with \(a_1a_2a_3=1\). The Galois group embeds into the even signed permutation group of order \(6\cdot4=24\); since the splitting field has degree 24, this embedding is onto. At a completely split prime away from the discriminant, every ordered triple of distinct opposite pairs with product 1 is therefore realized by reduction at a prime ideal of the splitting field.

For a nonzero residue \(v\), write \(b_p(v)=0\) for a square and 1 for a nonsquare. Here are four witnesses, with columns \(-1,q(a_1),q(a_2),q(a_3)\):

| p | Reduced triple | Symbol bits |
|---:|---|---|
| 83 | (18,32,33) | 1,0,1,0 |
| 83 | (18,33,32) | 1,0,0,1 |
| 83 | (32,18,33) | 1,1,0,0 |
| 307 | (39,132,147) | 1,1,0,1 |

Each triple has product 1 modulo p and its six signed entries are distinct roots of H. Both primes are away from the discriminant. The four rows have rank 4 over F2: the sum of the second, third and fourth rows is (1,0,0,0), which together with the first three rows spans the four coordinate vectors. Any square-class relation would reduce to a square at all four prime ideals (all radicands are units there), hence its exponent vector would be orthogonal to all four rows. It must be zero. Thus the four classes are independent over N.

The Kummer kernel of \(M=N(i,\sqrt{q(a_1)},\sqrt{q(a_2)},\sqrt{q(a_3)})\) over N is consequently the full group of 16 sign choices. Explicitly, the restriction map from Gal(M/Q) onto Gal(N/Q) has kernel Gal(M/N), of order exactly 16; each fiber is a coset of this kernel. M is Galois over Q because q(-a)=-q(a) and i belongs to M. Over the identity Frobenius of N the four signs are uniform, hence the three pair signs are jointly uniform conditional on the sign of -1 being +1. For a two-fixed-root element, choose one lift to Gal(M/Q). Multiplying it by the Kummer kernel independently toggles the sign on i and on the square root of q at the fixed root, giving uniformity of that pair sign conditional on the sign of -1. Chebotarev counts conjugacy-invariant events, so these fiber counts give the stated density table. No F.5 rank-10 assertion is needed for this deduction.

The original 9590-prime counts are **Observed (reported)**; the original Magma script is not archived here. This proof concerns available roots, not orbit accessibility or Problem H.

**Review update:** Claude independently checked the four residue witnesses and rank in `code/verify/pr87_four_witnesses.py`, with output in `notes/data/pr87_four_witnesses_output.txt` (commit `1c92e35`, review comment `7144691288`). This is AI verification, not human review. The prior request to establish joint uniformity via F.5 is superseded by the direct certificate.
