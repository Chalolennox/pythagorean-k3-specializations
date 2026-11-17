<!-- Provenance: uploaded to the chat by the repository owner on 17 November 2026 as gap_three_independent_review (1).md. Reviewed in notes/REVIEW_2026-11-17_gap_three_dossier.md; the checks are in code/verify_gap_three.py.
     The text below the line is unmodified. -->

---

# Independent review request: universal gap-three exclusion in Problem H

**Status:** Proposed computer-assisted theorem. Exact Magma V2.30 computations have been reported; the proof and implementation need independent verification before publication.

## 1. Claim under review

Let

\[
C/\mathbb Q:\quad y^2=x^3-2x^2+2x,\qquad P=(1,1),\quad T=(0,0).
\]

For each prime \(p\ge5\), let \(m_p=\operatorname{ord}(P\bmod p)\). For \(\varepsilon\in\{0,1\}\), put \(Q_{n,\varepsilon}=nP+\varepsilon T\) over \(\mathbb F_p\), and \(t(Q)=1-x(Q)\) for finite points. Define \(R_{p,\varepsilon}\subset\mathbb Z/m_p\mathbb Z\) by the qualifying criterion below.

**Proposed theorem:**

\[
R_{p,\varepsilon}\cap(R_{p,\varepsilon}-3)=\varnothing
\quad\text{for all primes }p\ge5\text{ and }\varepsilon=0,1.
\]

Thus no prime qualifies at two indices separated by three in the same orbit branch.

## 2. Exact qualifying criterion used in the computations

Set

\[
H(t)=t^6-30t^4-24t^2-1,\quad
x=1-t,\quad d=1+t^2,
\]
\[
q=\frac{2t(1-t^2)}{d^2},\qquad r=(1-t)d.
\]

A finite point \(Q\in C(\mathbb F_p)\) is declared **qualifying** precisely when:

1. \(H(t(Q))=0\) and \(d\ne0\);
2. \(q\ne0\) and \(r\ne0\);
3. \(q\) and \(r\) are squares in \(\mathbb F_p\);
4. **if** \(2\) is a square in \(\mathbb F_p\), then \(x\) must also be a square.

The computations used Magma `IsSquare`, including zero exclusions as stated. An independent reviewer should verify that these conditions are exactly equivalent to the intended arithmetic definition of a *qualifying prime*, rather than merely necessary conditions. The proposed gap-three exclusion follows for this explicitly stated finite-field criterion regardless of that interpretation.

## 3. Translation by \(3P\)

The known point is

\[
3P=\left(\frac{49}{9},-\frac{287}{27}\right).
\]

The reported addition formula is

\[
x(Q+3P)=\frac{A(x)+1722y}{D(x)},\qquad
A(x)=441x^2+799x+882,\quad D(x)=(9x-49)^2.
\]

**Reviewer check:** verify this identity against the group law on \(C\), including its domain of validity and points where \(D=0\). The later finite-field classification uses the actual elliptic-curve group law at every candidate, so denominator-zero cases are not silently discarded.

Write

\[
h(x)=H(1-x)=x^6-6x^5-15x^4+100x^3-189x^2+162x-54,
\quad f(x)=x^3-2x^2+2x.
\]

Let \(W=D-A-1722y\). In \(\mathbb Q[x,y]/(y^2-f(x))\), set

\[
G=W^6-30W^4D^2-24W^2D^4-D^6=G_0(x)+G_1(x)y.
\]

Then

\[
N(x)=G_0(x)^2-f(x)G_1(x)^2,
\quad R_3=\operatorname{Res}_x(h(x),N(x)).
\]

For computational efficiency, \(G_0,G_1,N\) were reduced modulo \(h(x)\) before the resultant was taken. This leaves the resultant unchanged because \(h\) is monic. Magma reported \(\gcd(h,D)=1\) over \(\mathbb Q[x]\) and \(\deg(N\bmod h)=5\).

## 4. Exact resultant reported by Magma

Magma V2.30 reported \(R_3\ne0\) and

\[
\begin{aligned}
|R_3|={}&2^{18}3^{45}7^2 71^2 307^{12}397^2\\
&\cdot4919^2\cdot8887^2\cdot19427\\
&\cdot7743563^{12}\cdot206215327\\
&\cdot49831710601^2\\
&\cdot286414695690956651258188903406027^2.
\end{aligned}
\]

Reported sign: negative. The denominator of the rational resultant was 1.

Consequently, subject to verification of the elimination and the characteristic-dependent denominator cases, a simultaneous polynomial zero at a prime \(p\ge5\) must occur at one of the eleven listed prime divisors:

\[
7,71,307,397,4919,8887,19427,7743563,
206215327,49831710601,
286414695690956651258188903406027.
\]

**Important subtlety:** A nonzero rational resultant does not, by itself, settle every issue concerning points where a denominator vanishes modulo \(p\). The finite-field group-law checks and the correctness of the implication from simultaneous qualifying points to the resultant divisibility must both be audited.

## 5. Finite-field candidate classification

A first test of the polynomial condition, using the displayed rational addition formula, gave:

| Prime | First geometric test |
|---:|---|
| 7 | eliminated |
| 71 | 2 polynomial coincidences |
| 307 | denominator-zero root (not resolved by rational formula) |
| 397 | eliminated |
| 4919 | eliminated |
| 8887 | eliminated |
| 19427 | 1 polynomial coincidence |
| 7743563 | denominator-zero root (not resolved by rational formula) |
| 206215327 | 1 polynomial coincidence |
| 49831710601 | 2 polynomial coincidences |
| 286414695690956651258188903406027 | 2 polynomial coincidences |

The seven non-eliminated candidates were subsequently checked by constructing points \(Q\in C(\mathbb F_p)\), computing \(Q+3P\) by Magma's **elliptic-curve group law**, and applying the qualifying criterion at both endpoints.

| Prime | Geometric pairs | Pairs satisfying both qualifying tests |
|---:|---:|---:|
| 71 | 2 | 0 |
| 307 | 0 | 0 |
| 19427 | 1 | 0 |
| 7743563 | 0 | 0 |
| 206215327 | 1 | 0 |
| 49831710601 | 2 | 0 |
| 286414695690956651258188903406027 | 2 | 0 |

The four primes eliminated in the initial geometric test were not rerun in this second script. The two tests together yielded **no surviving prime**. Neither script needed discrete logarithms or orders of points at the large candidate primes.

An earlier independent brute-force orbit test found **no gap-three pairs for any of the 9,590 primes** \(5\le p\le100000\) on either branch. This is corroboration, not a substitute for the global elimination argument.

## 6. Proposed deduction

If both \(Q_{n,\varepsilon}\) and \(Q_{n+3,\varepsilon}\) qualify, then their coordinates give a simultaneous zero of the two defining functions, and \(Q_{n+3,\varepsilon}=Q_{n,\varepsilon}+3P\). The exact resultant restricts the prime to the finite candidate list. The candidate checks rule out a pair satisfying both qualifying conditions. This proves the claimed exclusion, **provided the reviewer confirms the elimination covers every reduction and denominator case**.

With \(I_{p,\varepsilon}(n)=\mathbf 1_{n\in R_{p,\varepsilon}}\), the claimed exclusion implies

\[
I_{p,\varepsilon}(n)I_{p,\varepsilon}(n+3)=0.
\]

For \(h_{p,\varepsilon}(n)=1-2I_{p,\varepsilon}(n)\) and \(\delta_{p,\varepsilon}=|R_{p,\varepsilon}|/m_p\), this yields the exact local identity

\[
\frac1{m_p}\sum_{n\bmod m_p}
 h_{p,\varepsilon}(n)h_{p,\varepsilon}(n+3)
 =1-4\delta_{p,\varepsilon}.
\]

This is a **local** correlation statement, not a proof of independence of global root numbers or of the original rank-specialization problem.

## 7. Specific requests for independent review

1. **Check the group-law formula:** Is the displayed expression for \(x(Q+3P)\) correct for \(C\) and the given \(3P\)?
2. **Check the norm/resultant construction:** Is the polynomial \(G\) the correct denominator-cleared version of \(H(1-x(Q+3P))\)? Does reduction modulo \(h\) preserve the resultant exactly?
3. **Verify the resultant factorization independently** and check primality of the reported factors (especially the largest one).
4. **Audit bad characteristics and denominators:** Are all primes \(p\ge5\) covered, including those for which \(D\equiv0\) at a root or the translation point has unusual reduction?
5. **Recheck the seven finite-field tests**, including both square roots of each \(f(x)\), the point at infinity, and the group-law computation.
6. **Verify the qualifying criterion:** Does it agree with the intended original split-multiplicative condition? If not, state precisely what the computational theorem actually proves.
7. **Assess whether the result is a rigorous computer-assisted theorem**, and suggest a compact reproducible certificate suitable for a paper.

**Desired verdict:** Valid / valid after specific corrections / unproved, with an explicit counterexample or missing step where possible.

## 8. Computational environment

Reported calculations: Magma V2.30-1, exact rational polynomial arithmetic and finite-field elliptic-curve arithmetic. The user-provided outputs include a complete resultant factorization, candidate classification, and zero locally qualifying pairs for the seven remaining candidates. The computations have not yet been independently reproduced by the reviewer.
