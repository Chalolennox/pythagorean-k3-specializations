# Orbit-free split/non-split root densities for Problem H

**Status:** Corollary using the Galois and square-class calculations in \`paper/paper.md\`, Appendix F.2–F.7. The table below follows from the stated independence assertions. It does **not** prove a global root-number distribution along an elliptic orbit.

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

By the square-class computation of F.5, the quadratic character \((-1/p)\) is independent of the splitting field. For \((-1/p)=-1\), each fixed opposite pair contributes one split and one non-split root. For \((-1/p)=+1\), the two roots of each fixed pair have the same character.

On the two-root class, that pair character is equidistributed. On the six-root class, the three pair characters are jointly uniform in \(\{\pm1\}^3\), using the three \(q(a_i)\) characters in F.5 and their single relation with the other characters. This joint-uniformity deduction should be checked independently in review.

Thus the joint natural densities are:

| \(S_p\) | \(N_p\) | Natural density | Observed primes \(5\le p\le100000\) |
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

**Review request:** Check the joint uniformity of the three \(q(a_i)\) characters on the six-root Frobenius class against the full relation in Appendix F.5 before incorporating the density table as a proved corollary in the main paper.
