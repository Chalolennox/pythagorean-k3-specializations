# Problem H: finite-prime parity and exact CRT correlations

**Status: Observed** (finite computations with exact rational arithmetic). **Problem H remains open.**

## Setup

On (C:y^2=x^3-2x^2+2x), let (P=(1,1)), (T=(0,0)), and consider (Q_n=nP) or (nP+T). Set (t_n=1-x(Q_n)). For a prime (p\ge5), define a split event (X_p(n)=1) when

[
H(t_n)=t_n^6-30t_n^4-24t_n^2-1=0\pmod p
]

and (g(t_n)=2t_n(1-t_n^2)) is a nonzero square modulo (p). The event is absent at the identity of (C(\mathbf F_p)). In the computations, primes where (H) has repeated roots modulo (p) are excluded.

Write (m_p=\operatorname{ord}(P\bmod p)), (S_p\subseteq\mathbf Z/m_p\mathbf Z) for split-event residues, and (q_p=|S_p|/m_p). For a finite prime set (S), compare the exact period-average
[
M_S=\mathbb E_n\prod_{p\in S}(1-2X_p(n))
]
with the independence model (I_S=\prod_{p\in S}(1-2q_p)). The expectation in (M_S) is over the full least-common-multiple period, not over a random sample.

## Exact arithmetic method

For two primes, the joint probability is
[
\Pr(X_p=X_q=1)=
\frac{\#\{(a,b)\in S_p\times S_q:a\equiv b\pmod{\gcd(m_p,m_q)}\}}
{\operatorname{lcm}(m_p,m_q)}.
]
Thus coprime periods imply exact pairwise independence. For larger sets, generalized CRT compatibility and inclusion-exclusion give the exact mean:
[
M_S=\sum_{J\subseteq S}(-2)^{|J|}
\Pr(X_p=1\text{ for all }p\in J).
]
The Magma program computes these probabilities by recursively combining compatible congruence classes, avoiding enumeration of the full period.

## Empirical parity means

For (N=10^6) consecutive orbit indices and prime bound (B=20000):

| Branch | Empirical parity mean | Independence model | Difference |
|---|---:|---:|---:|
| (nP) | 0.440014 | 0.441209762624 | -0.001195762624 |
| (nP+T) | 0.531654 | 0.533489223032 | -0.001835223032 |

These are finite-sample observations; they are not exact full-period averages for all primes (p\le B).

## Exact ten-prime experiments

For each branch, the ten primes of largest split-event frequency among (p\le20000) were selected separately.

- (nP): 83, 547, 307, 149, 197, 757, 823, 631, 9391, 2293.
- (nP+T): 83, 673, 1009, 557, 617, 397, 823, 491, 1229, 1289.

| Quantity | (nP) | (nP+T) |
|---|---:|---:|
| Independent mean | 0.589065853008687908 | 0.722544543508531264 |
| Exact CRT mean | 0.583861991833028829 | 0.718215686108091026 |
| Exact minus independent | -0.005203861175659079 | -0.004328857400440238 |
| Centered pair correction | -0.005107322187142812 | -0.004424217331220565 |
| Centered triple correction | -0.000095609282015247 | +0.000090840965596145 |
| Orders 4–10 combined | -0.000000929706501021 | +0.000004518965184182 |

The joint periods were 30500933513870820 and 504444107807640. The exact inclusion-exclusion computations used 11645 and 13837 recursive nodes respectively, and 5195 and 5817 compatible terminal states.

For these *particular ten-prime sets*, pair corrections explain approximately 98.1% and 102.2% of the total departure from the independent model; the second value exceeds 100% because higher-order contributions partially cancel the pair correction. This is not a uniform theorem about larger prime sets.

## Interpretation and limitation

The near-independent finite-prime behavior has an explicit arithmetic source of deviation: split-event residue classes are constrained by common divisors of the local orbit periods. Exact pairwise correlations dominate the measured correction in these two selected ten-prime sets; the combined contributions from orders 4 through 10 are small.

**This does not establish global sign equidistribution or Problem H.** There is no proved control of the contribution of primes beyond the finite cutoff, nor a uniform correlation estimate as the cutoff grows. The exact finite-prime correlation calculation is complete for the selected ten-prime sets; an additional signed-increment experiment is ongoing. Problem H remains open.

## Reproducibility and provenance

Computed by the user in Magma V2.30-1 on 23 November 2026 from ChatGPT-proposed scripts. The exact ten-prime CRT computation completed in approximately 0.2 seconds; the million-index two-branch computation completed in approximately 23.5 seconds. No independent implementation or human verification is claimed. The accompanying Magma script reproduces the exact ten-prime means; the empirical million-index figures are transcribed from the user's execution log.

## Addition formula and signed-flip experiment (23 November 2026)

**Status: Observed**, with an exact finite-sample identity. For a block of new primes ((B,C]), let (F_{B,C}(n)=1) when that block produces an odd number of split events. Then
[
\sigma_C(n)=\sigma_B(n)(1-2F_{B,C}(n)),\qquad
M_C(N)-M_B(N)=-2\,\mathbb E_N[\sigma_B F_{B,C}].
]
Writing (A) for the number of indices with old sign (+1) and (F=1), and (D) for old sign (-1) and (F=1), gives the exact identity
[
M_C(N)-M_B(N)=2(D-A)/N.
]
An equivalent covariance decomposition is
[
M_C-M_B=-2\big(M_B\,\mathbb E_N[F]+\operatorname{Cov}_N(\sigma_B,F)\big).
]
The cancellation ratio (R=|D-A|/(A+D)) measures the net sign change per flipped index, not the covariance by itself.

For **N=100000**, the completed Magma V2.30-1 run reported:

| Branch | Prime interval | Positive-to-negative A | Negative-to-positive D | Flip fraction | Cancellation ratio | Mean after block |
|---|---|---:|---:|---:|---:|---:|
| (nP) | 5–1000 | 20209 | 0 | 0.20209 | 1.000000 | 0.59582 |
| (nP) | 1001–5000 | 5785 | 1439 | 0.07224 | 0.601606 | 0.50890 |
| (nP) | 5001–20000 | 5288 | 1818 | 0.07106 | 0.488320 | 0.43950 |
| (nP) | 20001–100000 | 4925 | 2240 | 0.07165 | 0.374738 | 0.38580 |
| (nP+T) | 5–1000 | 13352 | 0 | 0.13352 | 1.000000 | 0.73296 |
| (nP+T) | 1001–5000 | 8009 | 1429 | 0.09438 | 0.697182 | 0.60136 |
| (nP+T) | 5001–20000 | 4467 | 1101 | 0.05568 | 0.604526 | 0.53404 |

The original computation timed out after 299.6 seconds while processing the final (nP+T) interval. **No value is reported for that missing interval.**

On the (nP) branch, flip frequencies remain around 7.1% in the last three intervals while the cancellation ratio decreases from 0.602 to 0.375. This is a finite-sample pattern, not evidence of a limiting cancellation theorem: part of the reduction is expected from the evolving bias of the old sign. The covariance decomposition separates that baseline effect from arithmetic dependence.

The follow-up standalone program `code/magma/problem_h_optimized_addition.m` replaces full-orbit scans by sextic-root filtering and baby-step/giant-step searches, shares the elliptic-curve setup between branches, prints results at each cutoff, and performs small-prime direct-orbit regression checks. **The optimized program has not yet been run independently**; the above table comes from the earlier completed portions of the user's run.
