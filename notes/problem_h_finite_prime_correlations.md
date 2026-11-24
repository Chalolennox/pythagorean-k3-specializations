# Problem H: finite-prime parity and exact CRT correlations

**Status: Observed** (finite computations with exact rational arithmetic). **Problem H remains open.**

## Setup

On $C:y^2=x^3-2x^2+2x$, let $P=(1,1)$, $T=(0,0)$, and consider $Q_n=nP$ or $nP+T$. Set $t_n=1-x(Q_n)$. For a prime $p\ge5$, define a split event $X_p(n)=1$ when

$$
H(t_n)=t_n^6-30t_n^4-24t_n^2-1=0\pmod p
$$

and $g(t_n)=2t_n(1-t_n^2)$ is a nonzero square modulo $p$. The event is absent at the identity of $C(\mathbf F_p)$. In the computations, primes where $H$ has repeated roots modulo $p$ are excluded.

Write $m_p=\operatorname{ord}(P\bmod p)$, $S_p\subseteq\mathbf Z/m_p\mathbf Z$ for split-event residues, and $q_p=|S_p|/m_p$. For a finite prime set $S$, compare the exact period-average
$$
M_S=\mathbb E_n\prod_{p\in S}(1-2X_p(n))
$$
with the independence model $I_S=\prod_{p\in S}(1-2q_p)$. The expectation in $M_S$ is over the full least-common-multiple period, not over a random sample.

## Exact arithmetic method

For two primes, the joint probability is
$$
\Pr(X_p=X_q=1)=
\frac{\#\{(a,b)\in S_p\times S_q:a\equiv b\pmod{\gcd(m_p,m_q)}\}}
{\operatorname{lcm}(m_p,m_q)}.
$$
Thus coprime periods imply exact pairwise independence. For larger sets, generalized CRT compatibility and inclusion-exclusion give the exact mean:
$$
M_S=\sum_{J\subseteq S}(-2)^{|J|}
\Pr(X_p=1\text{ for all }p\in J).
$$
The Magma program computes these probabilities by recursively combining compatible congruence classes, avoiding enumeration of the full period.

## Empirical parity means

**Observed (transcribed from the user's log; original script not included).** For $N=10^6$ consecutive orbit indices and prime bound $B=20000$:

| Branch | Empirical parity mean | Independence model | Difference |
|---|---:|---:|---:|
| $nP$ | 0.440014 | 0.441209762624 | -0.001195762624 |
| $nP+T$ | 0.531654 | 0.533489223032 | -0.001835223032 |

These are finite-sample observations; they are not exact full-period averages for all primes $p\le B$.

## Exact ten-prime experiments

For each branch, the ten primes of largest split-event frequency among $p\le20000$ were selected separately. These selected ten-prime full-period means are not directly comparable to the all-primes-through-20000 million-index means: both the prime sets and averaging procedures differ.

- $nP$: 83, 547, 307, 149, 197, 757, 823, 631, 9391, 2293.
- $nP+T$: 83, 673, 1009, 557, 617, 397, 823, 491, 1229, 1289.

| Quantity | $nP$ | $nP+T$ |
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

**This does not establish global sign equidistribution or Problem H.** There is no proved control of the contribution of primes beyond the finite cutoff, nor a uniform correlation estimate as the cutoff grows. The exact finite-prime correlation calculation is complete for the selected ten-prime sets; the signed-increment and sample-size experiments are completed as reported below. Problem H remains open.

## Reproducibility and provenance

Computed by the user in Magma V2.30-1 on 23 November 2026 from ChatGPT-proposed scripts. The exact ten-prime CRT computation completed in approximately 0.2 seconds; the million-index two-branch computation completed in approximately 23.5 seconds. The AI reviewer independently reproduced the ten-prime means using Python (see review comment 7141240484); no human proof verification or independent Magma rerun is claimed. The accompanying Magma script is intended to reproduce the exact ten-prime means; the empirical million-index figures are transcribed from the user's execution log.

## Addition formula and signed-flip experiment (23 November 2026)

**Status: Observed**, with an exact finite-sample identity. For a block of new primes $(B,C]$, let $F_{B,C}(n)=1$ when that block produces an odd number of split events. Then
$$
\sigma_C(n)=\sigma_B(n)(1-2F_{B,C}(n)),\qquad
M_C(N)-M_B(N)=-2\,\mathbb E_N[\sigma_B F_{B,C}].
$$
Writing $A$ for the number of indices with old sign $+1$ and $F=1$, and $D$ for old sign $-1$ and $F=1$, gives the exact identity
$$
M_C(N)-M_B(N)=2(D-A)/N.
$$
An equivalent covariance decomposition is
$$
M_C-M_B=-2\big(M_B\,\mathbb E_N[F]+\operatorname{Cov}_N(\sigma_B,F)\big).
$$
The cancellation ratio $R=|D-A|/(A+D)$ measures the net sign change per flipped index, not the covariance by itself.

For **N=100000**, the completed Magma V2.30-1 run reported:

| Branch | Prime interval | Positive-to-negative A | Negative-to-positive D | Flip fraction | Cancellation ratio | Mean after block |
|---|---|---:|---:|---:|---:|---:|
| $nP$ | 5–1000 | 20209 | 0 | 0.20209 | 1.000000 | 0.59582 |
| $nP$ | 1001–5000 | 5785 | 1439 | 0.07224 | 0.601606 | 0.50890 |
| $nP$ | 5001–20000 | 5288 | 1818 | 0.07106 | 0.488320 | 0.43950 |
| $nP$ | 20001–100000 | 4925 | 2240 | 0.07165 | 0.374738 | 0.38580 |
| $nP+T$ | 5–1000 | 13352 | 0 | 0.13352 | 1.000000 | 0.73296 |
| $nP+T$ | 1001–5000 | 8009 | 1429 | 0.09438 | 0.697182 | 0.60136 |
| $nP+T$ | 5001–20000 | 4467 | 1101 | 0.05568 | 0.604526 | 0.53404 |

The original computation timed out after 299.6 seconds while processing the final $nP+T$ interval. The missing interval was subsequently completed by the optimized run below.

On the $nP$ branch, flip frequencies remain around 7.1% in the last three intervals while the cancellation ratio decreases from 0.602 to 0.375. This is a finite-sample pattern, not evidence of a limiting cancellation theorem: part of the reduction is expected from the evolving bias of the old sign. The covariance decomposition separates that baseline effect from arithmetic dependence.

The follow-up standalone program `code/magma/problem_h_optimized_addition.m` replaces full-orbit scans by sextic-root filtering and baby-step/giant-step searches, shares the elliptic-curve setup between branches, prints results at each cutoff, and performs small-prime direct-orbit regression checks. The optimized program was subsequently run by the user (see next section); no independent Magma rerun is claimed; the above table comes from the earlier completed portions of the user's run.

## Optimized addition-formula run: completed (23 November 2026)

**Status: Observed.** The user executed `code/magma/problem_h_optimized_addition.m` in Magma V2.30-1, N=100000, bounds 1000, 5000, 20000, 100000. Four direct-orbit versus BSGS regression tests passed: p=83 (period 39; event counts 4,2), p=149 (84; 2,0), p=197 (92; 2,0), p=307 (163; 4,0). All eight branch/cutoff exact addition-formula assertions passed. Wall-clock time reported: 8.7 seconds (Magma internal time 6s, memory 32.09 MB). The earlier unoptimized run timed out after 299.6 seconds.

The previously missing last interval, 20001–100000, on the nP+T branch was completed: 480 active split primes, A=5194 positive-to-negative flips, D=1682 negative-to-positive flips, flip fraction 0.06876, cancellation ratio 0.5107620709714951, covariance -0.0016005904, independent baseline contribution -0.0734411808, covariance contribution +0.0032011808, exact delta -0.07024, final mean 0.46380, independent-prime product 0.4600165260572131, difference +0.0037834739427869, and 7406 split-event occurrences.

For comparison, the final interval on nP had flip fraction 0.07165, cancellation ratio 0.37473831123517097, covariance -0.004640175, independent baseline -0.06298035, covariance contribution +0.00928035, delta -0.05370, final mean 0.38580, independent-prime product 0.3781597014893460, difference +0.0076402985106540.

The last-block covariance is negative for both branches and reduces the magnitude of the downward mean correction relative to independence between the old sign and the block flip indicator. The covariance changes sign across earlier blocks, so no monotonic or asymptotic covariance claim follows. These are finite-N truncated-sign results only; the global prime tail remains uncontrolled.


## Sample-size comparison at fixed prime cutoffs (23 November 2026)

**Status: Observed.** The user ran `code/magma/problem_h_covariance_sample_sizes.m` with N=10000, 50000, 100000, 250000, prime cutoffs 1000, 5000, 20000, 100000. Four small-prime BSGS/direct-orbit regressions passed; the addition formula passed at each cutoff. Magma V2.30-1 wall time 8.8s.

For the final prime block (20001–100000), empirical covariance of the old sign with the block-flip indicator was:

| N | nP covariance | nP+T covariance | nP final mean | nP+T final mean |
|---:|---:|---:|---:|---:|
| 10000 | -0.001301680000 | +0.000324080000 | 0.380800 | 0.450200 |
| 50000 | -0.004062129600 | -0.003262403200 | 0.383880 | 0.465920 |
| 100000 | -0.004640175000 | -0.001600590400 | 0.385800 | 0.463800 |
| 250000 | -0.004173728256 | -0.000371197120 | 0.385320 | 0.459928 |

At N=250000 the independent-prime products are 0.3781597014893460 $nP$ and 0.4600165260572131 $nP+T$, with empirical deviations +0.0071602985106540 and -0.0000885260572131. On the nP branch, the last-block covariance is roughly -0.004 for N>=50000; on nP+T it changes sign and magnitude across the tested N and has smaller absolute magnitude at N=250000 than at N=50000 or 100000; this does not imply convergence to zero. These finite samples do not establish limiting covariance or global parity distribution. Earlier-block covariances can also change sign (e.g. nP at 5001–20000: +0.0002144 at N=10000 versus -0.00142421728 at N=250000).

## Script availability and review

Three Magma-only scripts are included, outside the repository CI: exact ten-prime CRT (reported 0.2 s), `problem_h_optimized_addition.m` (8.7 s), and `problem_h_covariance_sample_sizes.m` (8.8 s). These are user-reported runtimes, not CI benchmarks. The million-index original script remains unavailable. See [AI review](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/88#issuecomment-7141240484). Documentation corrected with ChatGPT assistance; no new Magma run or human review.
