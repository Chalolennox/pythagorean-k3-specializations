# Mirror nonintersection in the rational circle traversal

Status: living draft; Proof given (not human-reviewed) for the arguments below; Observed for reported computations. Consolidated 24 November 2026. Written with ChatGPT assistance; no human proof review is recorded. This is a research note and a place to collect further results, not a claim about global root-number distribution.

## Setup

Let J/Q be y^2=x^3-2x^2+2x, P=(1,1), T=(0,0), and R=P+T. On the quotient J/{±1} define t(Q)=1-x(Q), extended to P^1 at the point at infinity. The mirror involution is M(t)=(t+1)/(t-1). Translation by T has x(Q+T)=2/x(Q), hence M(t(Q))=t(Q+T), including the projective extensions.

For k≠0, let G_k(a,b)=0 denote the symmetric projected correspondence of translation by kR. The explicit formula, writing u=x(kR), X=1-a and Z=1-b, is

G_k(a,b)=(X-u)^2 Z^2 + (-2u^2 X-2uX^2+8uX-4u-4X)Z +u^2X^2-4uX+4.

This is the general-gap correspondence already discussed in Appendix F.57 of paper/paper.md.

## Proposition: no rational mirror-paired parameter

For any nonzero integer k there is no t in P^1(Q) for which G_k(t,M(t))=0.

Proof. Choose Q over t (over an algebraic closure). The condition is x(Q±kR)=x(Q+T); replacing k by -k if needed, either kR=T or 2Q=-kR-T. The first is impossible since R has infinite order. If t is rational, x(Q) is rational; we must show the second equation has no solution even with rational x(Q).

If t(Q) is rational, x(Q) is rational, so for every σ in Gal(Qbar/Q), σ(Q)=Q or -Q. In the second case, 2Q=-kR-T=:C is a non-torsion rational point (as R has infinite order). Applying σ gives 2σ(Q)=C. If σ(Q)=-Q, then C=-C, a contradiction. Therefore every conjugate fixes Q: Q is rational. (This elementary Galois argument also applies to points with rational x and non-torsion rational doubles.)

If k=2m, 2(Q+mR)=T. But a rational point S with 2S=T would satisfy x(S+T)=x(S), hence x(S)^2=2, impossible over Q.

If k=2m+1, -kR-T=-kP-2(m+1)T=-kP, so after adding mP to Q one obtains 2(Q+mP)=-P. The duplication equation x(2S)=1 has numerator (x^2-4x+2)(x^2+2), with no rational roots. Thus P is not twice a rational point.

Both parities are excluded, including projective boundary parameters. This proves the proposition for rational *parameters*, not merely rational elliptic points.

## Observed computations (reported, scripts not yet archived)

Magma V2.30-1 checked the exact torsion-translation identity and the mirror-polynomial rational roots for k=1,...,12. No rational affine mirror-pair roots were found. For odd k=1,3,5,7,9,11 the quartic factors as two quadratics over Q; for even k=2,4,6,8,10,12 it was irreducible. These are finite observations, not an all-k factorization theorem.

The boundary t=1 gives a repeated projected neighbor for every k, since it corresponds to T=-T. Fixed-point equations G_k(t,t)=0 have rational roots at even gaps in the tested range (Observed).

## Scope and further collection

The reflection M(t) is not the sign reflection t -> 2-t (which exchanges 1-x and 1+x); keep these two involutions distinct. Mirror nonintersection does not imply disjointness of full orbit images, nor global root-number parity independence. Record new results and corrections in this note; use PR discussion for review and coordination.


## Theorem: limiting real mirror-pair distribution

For each integer k≥1, the equation 2Q=-kR-T has exactly two real solutions Q on J(R), hence two real projected parameters t_{k,1}, t_{k,2}=1-x(Q). Let

I = integral_{0}^{infinity} dx / sqrt(x(x^2-2x+2)) = 4.03646165391164... .

Then for every bounded continuous function f on (-infinity,1],

lim_{N→infinity} (1/(2N)) sum_{k=1}^N [f(t_{k,1})+f(t_{k,2})]
 = (1/I) integral_{-infinity}^{1} f(t) dt / sqrt((1-t)(1+t^2)).

Thus the limiting density is rho_t(t)=1/[I sqrt((1-t)(1+t^2))] for t<1, and zero for t>1. The support is (-infinity,1] (or its closure in the projective line). In the angular coordinate theta=2 arctan(t) mod 2pi, the density is

rho_theta(theta) = sqrt(1+tan(theta/2)^2) / [2I sqrt(1-tan(theta/2))]

on theta in [0,pi/2) union (pi,2pi), zero on (pi/2,pi); endpoints are understood in the integrable/a.e. sense. The support's closed accessible arc is [0°,90°] union [180°,360°]. Hence the real algebraic mirror parameters are dense on this arc but **not** on the entire circle.

**Proof.** The cubic x((x-1)^2+1) has only one real zero, so J(R) is a connected compact circle group. Choose H,U∈J(R) with 2H=-R and 2U=-T. The two real solutions for each k are Q_{k,0}=kH+U and Q_{k,1}=kH+U+T. As R has infinite order, H has infinite order, and each sequence is an irrational rotation, equidistributed in Haar measure. The x-map is continuous into the projective real line; its affine pushforward has density rho_x(x)=1/[I sqrt(x(x^2-2x+2))] for x>0. Indeed, the two y-branches each contribute |dx/(2y)| and the total normalization is I. Substitute t=1-x and then t=tan(theta/2). For bounded continuous f on the noncompact affine interval, the statement follows from equidistribution by extending f∘(1-x) to the compact curve except possibly at the identity, a Haar-null point; boundedness permits the standard Riemann-integrable version of Weyl equidistribution.

**Independent numerical check.** Magma V2.30-1 enumerated k=1..100 (200 real solutions). The maximum angular gap was 90.0229411267° at k=30 and remained unchanged through k=100; this reflects the forbidden 90° arc. Uniform-circle discrepancy at k=100 was 0.1600318627. Numerical quadrature of the theoretical Fourier magnitudes |c_m|, where c_m=(1/I)∫_0^∞ exp(2im arctan(1-x)) dx/sqrt(x(x²-2x+2)), yields m=1..5: [0.0493846069, 0.2867730794, 0.3540774667, 0.2243687909, 0.0066556477]. Observed Magma magnitudes at k≤100: [0.0556968370, 0.2910003918, 0.3629540430, 0.2015406386, 0.0254712283]. Numerical agreement supports the exact formula; no convergence rate is claimed.

**Scope.** This is a theorem about real algebraic parameters and elliptic Haar measure, not about global root numbers or rational rank jumps.


## Consolidated research register

The central objective is Problem H, not the geometry alone. This note distinguishes characteristic-zero correspondence geometry from finite-field eligible-prime arithmetic. See [workflow policy](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/83#issuecomment-7143265860) and paper Appendix F.57. The figure [eligible-prime rectangle](figures/eligible_prime_rectangle.svg) is schematic, not an independent proof.

**Verification convention:** Proof given means an argument is supplied but not human-reviewed. Observed means a reported computation; scripts and raw outputs are not yet archived here unless explicitly stated. Conditional means a dependency is outstanding. The historical comments linked below are provenance, not authority over corrections in this note. No Magma, SAT or CI run was performed during this consolidation.

### Principal arithmetic result and proof certificate

Let D be the twelve geometric points on J with h(x)=H(1-x)=x^6-6x^5-15x^4+100x^3-189x^2+162x-54=0, where H(t)=t^6-30t^4-24t^2-1. For p>=5 let Q(n) be the set of primes at which nP reduces into D and 2t(1-t^2) is a nonzero square. The reported exact exceptional-prime classification is Q(n) ∩ Q(m) ∩ Q(n+m) ⊆ {609613}. For the full group generated by P,T the exceptional set is {609613,1386618529213}. This is a computationally supported proof claim, not yet independently certified in full. The characteristic-zero no-triple theorem for G_k is separate and cannot establish this arithmetic claim by itself.

For distinct x,z define Y=x^3-2x^2+2x, q=(h(z)-h(x))/(z-x), B=(u-2+x+z)(x-z)^2-Y(x)-Y(z), F=(B^2-4Y(x)Y(z))/(x-z)^2. The addition formula implies F=0 when u is the x-coordinate of the sum. Eliminate z with Res_z(q,F), then x with h(x), then u with h(u). For equal x the opposite-point case sums to O and the doubling case uses x(2Q)=(x^2-2)^2/(4Y(x)). Include primes dividing disc(h) and Res(h,Y) in the exceptional checks. The exact resultant factorization and finite-field accessibility certificate are recorded below. At p=609613 the user independently verified the order, eligible residues and additive triples in Magma. The other exceptional-prime exclusions still need standalone reproducible certification.

### Research disposition

- Geometry: retain mirror nonintersection, halving factorization, intersection arrangement and real/modular distribution as Proof given.
- Isogeny route: retain supplied arguments as Proof given, subject to review of modular-curve dependencies.
- Synchronization, adaptive contraction, prefix words, subgroup avoidance and multiplier lattices: explored; no global parity result. Do not repeat without a new mechanism.
- Singleton route: distinguished prime recurrence is exact, but a singleton through 10^8 is not a complete singleton. Doubling excludes old competitors other than 609613 but does not exclude new ones.
- Binary return tree: exact affine rules A(z)=524288z+147895, B(z)=524288z+147896, n=85900+304516z. The finite-cutoff singleton path fails at depth two. Reachable SAT witnesses refute a uniform return bound of six at cutoff 20000; the finite-state upper bound is not uniform in the cutoff.
- Spectral route: local persistence is proved by the supplied linear-algebra argument; the locally finite sum counterexample prevents inferring global persistence from finite spectral separation. Close this route absent additional arithmetic control.
- Problem H remains Open. On the original traversal positive root number requires even eligible cardinality under the paper's root-number formula. Singleton recurrence is not itself the desired positive-sign conclusion.

### Corrections and outstanding verification

The competitor matrix in comment 7140630553 was retracted in 7140934814; do not use it. The reduced-coordinate constants in that latter comment were corrected in 7140938753. The execution provenance of the backward-DP comment 7141118069 is unsupported; its histogram is not certified. The non-torsion certificate in 7137144713 and 7137148348 is not verified and its reduction counts must be recomputed before using the canonical-height argument; the argument is conditional on positive common height. Earlier undocumented C++ claims are not promoted to verified computations; prefer the user Magma confirmations where available (7134398628, 7134576317, 7138177099, 7138495010). All other historical execution assertions are reported only, not fresh verification. The finite-field arrangement analogue requires distinct sign classes modulo ord(R); G_k may coincide at finite primes. No assertion about singularities of individual G_k is made. The independent AI reviews 7141240059 and 7142633781 did not certify the later arithmetic proofs or rerun the experiments.

### Consolidated arguments from the discussion

The following source-derived arguments are retained for review. Historical headings such as “theorem” or “exact” do not override the verification convention above. Computational statements within them are Observed, and the exceptional-prime classification remains subject to the certificate limitation above.

#### Source 7117054164 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7117054164)

##### Uniform proof of the observed odd/even factorization pattern (all nonzero gaps)

**New theorem (exact, not merely the k≤12 observation).** Let
\[
J:y^2=x^3-2x^2+2x,\quad P=(1,1),\quad T=(0,0),\quad R=P+T,
\]
and let \(F_k(t)\) be the degree-four *halving polynomial* for the mirror equation \(2Q=-kR-T\), expressed in \(t=1-x(Q)\). For every nonzero integer \(k\), \(F_k\) is squarefree, and:
- **odd k:** \(F_k\) factors over \(\mathbf Q\) as two irreducible quadratics;
- **even k:** \(F_k\) is irreducible over \(\mathbf Q\).

This upgrades the experimental observation for k=1,...,12 in the research note to a uniform statement.

**Proof.** We use that \(R=P+T\) and \(2T=0\).

For \(k=2m+1\), the equation becomes \(2(Q+mR)=-P\). Set \(V=Q+mR\). The x-coordinates of the four halves of \(-P\) are obtained at k=1 from
\[
F_1(t)=t^4-2t^2+8t-3=(t^2+2t-1)(t^2-2t+3).
\]
Each quadratic is irreducible over Q. Moreover, each half \(V\) is defined over its quadratic x-field: if a Galois automorphism fixed x(V) but negated V, it would negate the non-torsion rational point 2V=-P, impossible. Thus all four halves are defined over quadratic extensions. Translating by \(-mR\in J(\mathbf Q)\) preserves their fields. For \(Q\), the doubled point \(-kR-T\) is rational and non-torsion, so the same Galois argument implies \(\mathbf Q(Q)=\mathbf Q(x(Q))\). The x-coordinate therefore has degree 2, not 1 (the rational nonintersection theorem excludes degree 1). The four distinct roots consequently split into two irreducible quadratics.

For \(k=2m\ne0\), the equation becomes \(2(Q+mR)=T\). Put \(H=Q+mR\), so \(2H=T\). Since \(H+T=-H\) and \(x(H+T)=2/x(H)\), we obtain \(x(H)^2=2\). Substituting into the curve equation gives
\[
y(H)^2=4(x(H)-1).
\]
With \(z=y(H)/2\), this is \(z^4+2z^2-1=0\), which is irreducible over Q: \(z^2=\sqrt2-1\) is not a square in \(\mathbf Q(\sqrt2)\), because its norm is \(-1\). Hence each half \(H\) has degree 4 over Q. Translation by \(-mR\) preserves the point field, so \([\mathbf Q(Q):\mathbf Q]=4\). Since \(2Q=-kR-T\) is rational and non-torsion for k≠0, the Galois argument again yields \(\mathbf Q(Q)=\mathbf Q(x(Q))\). Thus every root \(t=1-x(Q)\) has degree 4, proving irreducibility. The four halves are distinct because multiplication by 2 is separable in characteristic zero. QED.

**Scope:** This concerns the exact mirror halving quartic \(F_k(t)\) (equivalently the properly reduced specialization of the projected correspondence). It does **not** establish correlations of bad-prime sets or global root-number parity.

**Relevant literature:** The general relationship between quartics and elliptic 2-division is treated in G. H. Hitching, *Quartic equations and 2-division on elliptic curves*, https://arxiv.org/abs/0706.4379; see also B. M. Bekker and Y. G. Zarhin, *The divisibility by 2 of rational points on elliptic curves*, https://arxiv.org/abs/1702.02255. The proof above is a specialization to this curve and does not claim a new general 2-division theorem.

#### Source 7125657801 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7125657801)

##### Exact intersection arrangement: reflection exclusion, pairwise classification, and no triple intersections

New Magma output (V2.30-1, gaps 1–20 and visible pairwise tests through the truncated output) agrees with the following group-law theorems. These are independent of Problem H.

**Reflection.** With X=1-t and u=x(kR), direct substitution Z=-X in the existing correspondence gives exactly X^4+4(u-1)^2 X^2+4. This is strictly positive for real X, and its homogenization is nonzero at infinity. Thus G_k(t,2-t)=0 has no real projective solution for any nonzero k.

**Pairwise intersections.** For distinct positive k,l, choose a lift Q of t. The two possible projected neighbors are π(Q±kR), where π=1-x. Equality with a neighbor for l forces 2Q=±(k+l)R or ±(k-l)R; changing Q to -Q removes the redundant signs. Each of the two non-torsion doubled targets has four halves with distinct x-coordinates, and the two x-sets are disjoint because the targets are not equal up to sign. Each such parameter has exactly one common neighbor (two common neighbors would require both halving conditions, or kR=±lR). No boundary intersections occur: a coordinate at infinity would force the other to equal π(kR)=π(lR). Thus there are eight distinct geometric intersections, four real (J(R) is connected and doubling has two real preimages per target; a real x above a real non-torsion doubled target forces a real point by conjugation). The squarefree monic resultant is the product of the two monic halving quartics. In fact the intersection number of two (2,2) divisors is eight, so all eight intersections have multiplicity one.

For equal parity, write a=(k+l)/2, b=(l-k)/2, k<l. The four rational ordered pairs are (π(aR+εT),π(bR+εT)) and their reversals, ε=0,1. These exhaust the rational pairs: rational x of a half of a rational non-torsion point forces a rational lift, and J(Q)[2]={O,T}. For opposite parity, a rational half would imply R∈2J(Q), impossible since x(R)=2 whereas the duplication formula x(2S)=(x(S)^2-2)^2/(4y(S)^2) is a rational square for finite non-torsion doubles.

**No triple intersections (over Qbar).** Given (t,w), choose lifts Q,U. Membership in G_k forces kR∈{±(U-Q),±(U+Q)}. Each sign class contains at most one positive multiple of the infinite-order point R. Hence at most two distinct positive-gap correspondences pass through any point, including projective boundary points. Together with the intersection number argument, every finite arrangement of these curves has only ordinary transverse pairwise crossings between distinct components. This statement does not address possible singularities of individual components.

These results are exact, not extrapolations of the numerical sample. No implication for global root-number parity or rank jumps is asserted.

#### Source 7125764420 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7125764420)

##### Joint limiting distribution of rational pairwise intersections

The rational intersections of G_k and G_l, 1≤k<l≤N of equal parity, are exactly (π(aR+εT),π(bR+εT)) and reversals, ε=0,1, with a=(l+k)/2, b=(l-k)/2. Thus (a,b) ranges bijectively over D_N={(a,b)∈Z²:1≤b<a, a+b≤N}. Its size is asymptotic to N²/4. No triple intersections means the resulting ordered pairs are counted without duplication.

**Theorem.** The empirical probability measure of all rational intersection pairs converges weakly on P¹(R)² to ν⊗ν, where ν=π_*μ_J is the Haar pushforward already described in this note. In affine coordinates the joint density is 1/[I² sqrt((1-t)(1+t²)(1-w)(1+w²))] for t,w<1, zero elsewhere, with I the normalization integral defined in the note. In angular coordinates the joint density is the product of the two previously derived angular densities. In particular the rational intersections are dense in the product of the accessible closed arcs, and the two angular coordinates are asymptotically independent (not uniform).

**Proof.** Identify J(R) with R/Z, R with irrational α and T with 1/2. For any nonzero integer character (r,s), sum exp(2πiα(ra+sb)) over D_N. If r≠0, fix b and sum over the contiguous interval of a; the geometric sum is bounded by 2/|1-exp(2πirα)|. There are O(N) rows. If r=0, sum over b first using s≠0. Dividing by |D_N| gives O_{r,s,α}(1/N). The simultaneous torsion shift multiplies the character by a constant of modulus one. Weyl's criterion gives Haar product measure; reversal preserves it, and the continuous projective projection gives the stated pushforward. This is a fixed-character bound, not a uniform discrepancy rate. For angular Fourier moments, the limit of exp(i(mθ+nφ)) is c_m c_n, where c_j is the one-dimensional angular Fourier coefficient. This theorem concerns real geometry of rational intersections, not arithmetic independence of root numbers or ranks.

#### Source 7125809848 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7125809848)

##### Finite-prime extension of joint intersection equidistribution

For a fixed finite set S of odd primes, let H=<R_S> in ∏J(F_p), L=lcm ord(R_p), and T_S the diagonal reduction of T. Within common torsion branch ε, the joint real/modular law of the rational pairwise intersections converges to (μ_J⊗u_{H+εT_S})^{⊗2}, before applying the projective parameter map. Proof: partition D_N={1≤b<a,a+b≤N} by a,b modulo L; each cell has size |D_N|/L²+O_L(N). On each cell the nontrivial real Fourier character sum is O_{L,r,s,α}(N), by geometric summation with irrational Lα. Coordinate reversal preserves the limit. Averaging branches yields the equally weighted mixture of these two product measures, NOT generally the product of the mixture marginals. Real angular positions remain independent of all finite modular data. For any finite modular observable f of the projected parameter (e.g. truncated qualifying-prime sign), write mε=L^{-1}Σ_{j mod L} f(π(jR_S+εT_S)). The limiting covariance between f at the two intersection coordinates is (m0−m1)²/4; their product mean is (m0²+m1²)/2. Thus shared torsion branch is an exact source of possible arithmetic correlation. Within each branch covariance vanishes. Distinct primes are not generally independent: admissible exponent residues j_p obey j_p≡j_q mod gcd(ord(R_p),ord(R_q)), by generalized CRT. The same proof works with reduction modulo fixed prime powers at good primes. None of this controls the unbounded-prime tail of global root numbers, or permits interchanging cutoff and traversal limits. General background: Kowalski, Introduction to Probabilistic Number Theory, Thm B.6.3 (compact abelian Weyl criterion), https://people.math.ethz.ch/~kowalski/probabilistic-number-theory.pdf .

#### Source 7126392819 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7126392819)

##### Single-valued rational transformation with intersections at every gap

Let π=1−x and f_d∘π=π∘[d], d≥2 (degree d²). Intersection G_k(t,f_d(t)) is equivalent, after choosing a lift, to (d−1)Q=kR or (d+1)Q=−kR. Rational t forces Q rational by the non-torsion rational target and Galois sign argument. In particular f_2(t)=1−(t²−2t−1)²/[4(1−t)(1+t²)] gives t=π(kR) for every positive k, with distinct non-diagonal rational pairs. The other branch is 3Q=−kR. Direct counting gives #J(F3)=6 and #J(F5)=8; R mod 3 has order divisible by 3 (x(2R)=1 mod 3, so 2R≠O), hence R is not 3-divisible over Q (3J(F3) has order at most 2). Also J(Q)[3]=0 by good reduction at 5. Consequently the second branch gives exactly one additional rational parameter π((k/3)R) iff 3|k. Thus the number of rational intersections with the duplication graph at gap k is 1+1_{3|k}. This is a traversal theorem, not a rank-jump theorem for E_t; multiplication covers elsewhere in the paper should not be conflated with it.

#### Source 7126426738 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7126426738)

##### Obstruction to transferring points via generic isogenies of the specialized family

The Lattès transformations on J do not induce generic isogenies on E. In fact for any nonconstant f∈Q(t), geometric isogeny of E_t and E_f implies j(t)=j(f(t)). Proof: j(t)=1728(t²−1)^3/H(t), H=t⁶−30t⁴−24t²−1, has six simple poles. Any isogeny can be factored through multiplication to obtain a cyclic isogeny of degree N. If N>1, its modular polynomial identity defines a nonconstant morphism P¹_t→X₀(N) over C (use normalization and extension of rational maps between smooth projective curves). The source j-map on X₀(N) has at cusp 0 pole order N: with τ=−1/z, local parameter exp(2πiz/N), j(τ)=j(z) has pole order N. Surjectivity then forces a pole of j(t) of order ≥N, contradiction. Thus N=1. Equality of j implies deg f=1. Its zero divisor consists of ±1 each of order 3, while j−1728 has double zeros at 0,∞ and simple zeros at ±i, as follows by subtracting the numerator and denominator. Hence f preserves {0,∞} and {±1}, forcing f=t,−t,1/t,−1/t. Inversion is excluded by j(2)≠j(1/2) (or by A→−A in the invariant expression). Only ±t remain. The negative symmetry is the already known −1 quadratic twist (paper §§5–7/F.46), not a generic Q-isogeny: a geometric isomorphism over Q(i)(t) is anti-invariant under conjugation and the generic endomorphism ring is Z because j is nonconstant. This is a generic obstruction, not a claim that isolated specializations cannot be isogenous. It also does not exclude multivalued correspondences or independent sections on covers. Reference for modular curve interpretation: https://math.mit.edu/classes/18.786/2024/LectureNotes19.pdf .

#### Source 7126462192 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7126462192)

##### Finiteness theorem for nontrivial rational isogeny correspondences

The multivalued rational-isogeny route can be closed unconditionally for distinct j-invariants. For each prime p let Y_p be the normalized pullback of X_0(p)→P¹_j along j(t). The six simple poles of j(t) give six local p-cycles of the degree p+1 cover. If disconnected over C, its monodromy orbits must have sizes p and 1; the singleton gives a section P¹_t→X_0(p), impossible since this nonconstant map is surjective and the width-p cusp would force a pole of j(t) of order ≥p. Hence Y_p is geometrically connected. Riemann–Hurwitz gives 2g−2≥−2(p+1)+6(p−1), so g≥2p−3 for p≥3. For p=2 the paper already proves finiteness via the genus-two curve y²=64+16c²−c⁶ (rational 2-torsion); alternatively the two simple preimages ±i of j=1728 supply two additional simple ramification contributions in the degree-three X_0(2) covering, giving g≥2. Faltings yields finitely many rational t for each prime. Mazur's prime-isogeny theorem restricts p to 2,3,5,7,11,13,17,19,37,43,67,163 (https://www.math.columbia.edu/~goldfeld/Mazur-Goldfeld1978.pdf). Any Q-isogeny between curves of distinct j factors, after removing multiplication, through a nontrivial rational cyclic isogeny and thus a rational prime-order subgroup. Therefore only finitely many family parameters can participate in Q-isogenies with distinct j, even allowing arbitrary multivalued correspondences. This extends the paper's existing p=2 finiteness, is ineffective, and does not address rank≥2 finiteness itself. For each source t the rational cyclic degree list of Mazur–Kenku is finite, with finitely many kernels per degree and finitely many w per target j; thus the set of ordered distinct-j isogenous parameter pairs is finite as well.

#### Source 7128028142 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7128028142)

##### Factorial synchronization: exact exclusion bound (limited consequence)
For Q_n=[n!]P on J and x(Q_n)=a_n/b_n² in lowest terms, put C_n=b_n¹²h(a_n/b_n²) as in F.18. For every p≥5 with d_p=ord(P mod p), d_p|n! implies Q_n reduces to O, hence p|b_n, p∤a_n and C_n≡a_n⁶≠0 mod p. Thus p|C_n implies d_p∤n!, in particular d_p>n and by Hasse p>(√n−1)². More precisely some prime ℓ satisfies v_ℓ(d_p)>Σ_{k≥1}floor(n/ℓ^k), so d_p contains a prime-power divisor exceeding n. This is a uniform exclusion of small multiplicative-reduction primes, not a parity theorem. F.18 still forces primes outside every fixed finite set to occur to odd exponent eventually. Factorial traversal preserves the known rank-one section and converges p-adically to O at every fixed prime (formal group), but no real convergence is asserted. No restriction on the parity of qualifying surviving primes follows. The height grows quadratically in n!, so direct factorization becomes rapidly impractical. The paper already contains the essential Faltings obstruction; the new observation is the explicit moving exclusion bound.

#### Source 7128362758 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7128362758)

##### Adaptive contracting traversal (existence, not parity control)
Unlike fixed translation, an adaptive integer step can produce geometric real convergence while preserving the rank-one cover. On connected J(R), normalized elliptic logarithm sends P to irrational α. Given rational target Q*, choose positive k with 0<d(Q+kP,Q*)<d(Q,Q*)/2; density guarantees existence. More concretely for target P and t*=0, start Q=2P and choose the least positive k with 0<|1−x(Q+kP)|<|1−x(Q)|/2, skipping O. This is an exact rational comparison and terminates by density; all parameters distinct, |t_n|≤(3/4)2^−n, and the cover is preserved. One may restrict k to multiples of any fixed L, or at stage n to multiples of a growing modulus, without losing density. This is an adaptive search, not a fixed rational algebraic contraction; no bound on global qualifying-prime parity follows. It is a constructive formulation of the real approximation mechanism, not a new rank-jump theorem.

#### Source 7129495712 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7129495712)

Split-character composition classification (hand proof): g(Q)=2x(x-1)(x-2), g(Q+T)=4g(Q)/x(Q)^4. Thus [g_{n,0}]=[g_{n,1}] for g_{n,e}=g(Q+nP+eT). Mod 2 divisor support is {(1-n)P,(-1-n)P,(1-n)P+T,(-1-n)P+T}; the zero at T before translation has multiplicity 2 and pole at O order 6. Any nonempty finite set of distinct indices has a unique extreme support point (-1-N)P for largest index N, proving independence even over Qbar(J). Consequently these mirror relations generate ALL finite square-class relations: rectangle dimension 2, exactly three nonempty square products (02,13,0123). For p>=5 multiplicative at either mirror member, the split character is identical when evaluated at either parameter (units there). However F.25 establishes disjoint discriminant prime supports on the two branches, so this does not cancel local root numbers: it only supplies a common character on two different prime sets. F.25/F.53 already give the periodic reciprocity-factor product (-1)^n, hence its rectangle product -1. No new global parity conclusion.

#### Source 7135709265 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7135709265)

Exact executed SymPy computation /tmp/triple.py proves D∩(D+D)=∅ in characteristic zero by good reduction at 5. Set f(x)=H(1−x), Y=x³−2x²+2x, B=(u−2+x+z)(x−z)²−Y(x)−Y(z), F=(B²−4Y(x)Y(z))/(x−z)². Over GF(5), f squarefree, Groebner basis of [f(x),f(z),f(u),(f(z)−f(x))/(z−x),F] in z,x,u is [1]. Equal x: opposite points sum to O; doubling gcd(f(x), resultant_u(f(u),4Y(x)u−(x²−2)²))=1 mod 5. Proper good reduction and monic f ensure any characteristic-zero triple specializes to a triple in D_5, impossible. Thus outside a finite exceptional prime set, no prime can be eligible simultaneously at Q,R,Q+R, uniformly in rational Q,R. D=−D gives subtraction too. Exceptional primes not yet determined, no implication for global parity. Web fetch of paper failed this turn; prior connector paper check showed F.17,F.19,F.57 related but distinct.

#### Source 7136747343 — Reported computational certificate

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7136747343)

Confirmed sum-free exceptional set by rerunning /tmp/exceptions.py and /tmp/checkexc.py and executing new /tmp/access.py (SymPy exact resultants, finite field enumeration, BSGS order and discrete logs with scalar multiplication verification). Candidate primes >=5: 7,19,23,31,71,83,229,797,5087,7351,12113,363773,609613,9624457993,1386618529213,49635479695149757. Distinct-coordinate resultant factors: 2^108 7^12 31^6 71^12 83^6 229^2 12113^2 609613^2 363773^2 5087^6 9624457993^2 49635479695149757^6 1386618529213^2. Doubling resultant: 2^36*19*229*797*12113*7351*609613*363773*9624457993*1386618529213. disc(f)=2^6*3^18*23^2 in absolute value. Only 229,609613,1386618529213 have eligible triples over F_p. BSGS: p229 ord P=36, none of four eligible points in <P,T>. p609613 ord P=304516, all four eligible points in <P>, logs ±42950,±85900, six ordered triples. p1386618529213 ord P=693308733824, eligible points logs ±27171863358 P, ±822156916 P, ±411078458 P+T; six ordered triples all involve mirror points, none entirely in <P>. Therefore exact exceptional set for triple intersection on original traversal is {609613}, and full <P,T> is {609613,1386618529213}. Witnesses Q=42950P at p609613 reduces to (508622,603262), 2Q=(100993,480535); R=411078458P+T at large prime reduces to (1316438545547,152107308206), 2R=(1244038125933,527140836946). Eligibility uses H=0 and nonzero square 2t(1−t²). Independent Magma certification still outstanding; no implication for global parity.

#### Source 7137270889 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7137270889)

Independent Magma V2.30-1 certification supplied by user: p=609613, #J(Fp)=609032, ord(P)=304516=4*76129, T outside <P>. All four eligible points accessible, residues [42950,85900,218616,261566], six ordered additive triples, doubling survivors ±42950, no two consecutive doubling survivals. New exact orbit result: starting ±42950 transient length 1, cycle length 19032, hits [0,1,9517] before first repetition; starting ±85900 transient 0, cycle length 19032, hits [0,9516]. Thus for seed 42950 and k>=1 eligibility iff k≡1 mod 9516; local negative-sign density 1/9516. The prime is not permanently eliminated but absent for 9515 consecutive steps between recurrent hits. This certifies local classification at this prime, not exhaustiveness of the global exceptional list or global parity. Magma CPU 0.380s.

#### Source 7137553270 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7137553270)

Unconditional simultaneous creation/disappearance under doubling: using previously computed eligible residue sets R83={12,16,23,27} mod39 and R149={16,68} mod84, CRT gives n≡874 mod1092 (n≡16 mod39,34 mod84). Then 83 is eligible at n but not 2n (32 mod39), while 149 is ineligible at n but eligible at 2n (68 mod84). CRT checked by Python. Thus infinitely many simultaneous prescribed prime exchanges, independent of H. General finite prescription criterion: choose residues in R_p\[2]^{-1}R_p for disappearance and [2]^{-1}R_q\R_q for creation, satisfying pairwise congruence modulo gcd of periods. No control of unprescribed primes or total parity. Local residue inputs from prior computations; not independently rerun here.

#### Source 7141490304 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7141490304)

User-executed reachability-constrained incremental PySAT: cutoff 20000, 156 active primes, L 275 digits, v2(L)=4, reachable states {0} union z≡7,8 mod16. Previous witness reachable. SAT for bounds 1..6, times .009,.012,.0139,.121,.4912,17.7545 s; verified witness waits 2..7 respectively. Depth6 witness blocks all126 words, 86 distinct competitors, 77/128 singleton endpoints at depth7. New rigorous finite-cutoff theorem: write L=16D odd D. A,B generate transitive permutation group modulo D (BA^-1 translation1). From any state choose positive-word prefix taking its odd coordinate to 0, length at most D-1 (shortest directed path). Append B; since multiplier 2^19 kills mod16, endpoint is congruent to B(0)=147896 mod L, known truncated singleton at cutoff20000. Hence every state reaches a singleton, and exact maximum positive waiting time among reachable singleton states satisfies 7<=K_20000<=D. This is finite-cutoff only; does not bound K uniformly across cutoffs or control prime tail. Recommend investigating parity rather than singleton as sufficient condition for H; no global proof.

#### Source 7141920329 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7141920329)

Cutoff-free local difference operator: user Magma tests d=1..256 confirm stable rank m−1 for d=2^e m odd m; original stabilization bound fails all even d, corrected bound 1+ceil(e/19) holds generally. Proof: after K=ceil(e/19) iterations every affine composition has multiplier divisible by 2^e, hence image consists of m-periodic functions. On odd-period space Delta=U(I+S), U permutation, constants kernel and zero-sum subspace invariant invertible. One further step removes constants; zero-sum subspace survives all powers, proving stable rank m−1. Higher identity Delta^k=U^k(I+S)^((2^(19k)−1)/(2^19−1)) verified by user Magma. Actual local functions p83,149,307,547,757 persistent; p197,631 identically zero on distinguished class. Global cancellation of locally finite sum remains unresolved. No prime cutoff used in theorem.

#### Source 7142146880 — Proof given / Observed where computational

[Discussion provenance](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7142146880)

Spectral decomposition: for odd m over algebraic closure F2, e_zeta(z)=zeta^z, Delta e_zeta=zeta^147895(1+zeta)e_(zeta^(2^19)). Exact frequency order preserved, every nontrivial block invertible. Finite sums cancel only within common frequency orders. Known periods 39,21,163,51,89 share only nontrivial order 3. Global obstruction: on nonnegative integers let g_j=indicator(z=-1 mod 3^j). g_j tends pointwise to zero and h_j=g_j+g_(j+1) has zero order-3 component (odd-index lifts preserve low-frequency Fourier coefficients), yet locally finite sum over j>=1 h_j=g_1 with nonzero order-3 component. Thus finite spectral projection does not commute with pointwise locally finite sums even for odd periods and support sizes of h_j equal 2 per period. Cannot isolate global arithmetic frequencies without additional uniform control. This is an abstract counterexample, not an arithmetic counterexample to H.

### Remaining discussion index (reported observations, proposals and review history)

- [7116732518](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7116732518): Open research question: arithmetic consequences of mirror nonintersection…
- [7116876931](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7116876931): New result from Magma: real algebraic mirror pairs (k=1..100)…
- [7125902478](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7125902478): Exact nonzero finite-cutoff covariance and numerical scale…
- [7128127645](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7128127645): Optimized synchronization: held-out prime test (Magma V2.30-1)…
- [7128199114](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7128199114): Constant-step synchronization: million-cutoff validation and recommended closure…
- [7128490278](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7128490278): Adaptive real contraction toward rank-two target: numerical conclusion…
- [7129299775](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7129299775): Symbolic composition obstruction: let h(x)=H(1-x), f_g(Q)=h(x(Q+g)) for g=0,P,T,P+T. Exact SymPy gcd computations give gcd(h,h')=gcd(h,x^3-2x^2+2x)=1. Write d=(x-1)^2, a=x^2-x+2, Y=x^3-2x^2+2x, and L(A,D)=D^6 h(A/D). Then gcd(h,L(2,x))=gcd(…
- [7129414587](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7129414587): Independent Magma V2.30-1 verification supplied by user: all five gcd tests and all fifteen nonsquare tests passed (888 ms). Geometric consequence: for any r selected functions, their simultaneous square-root cover has degree 2^r, 12r disti…
- [7129793200](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7129793200): Exact all-translation obstruction: (D-D)∩J(Q)={O}, where D is the 12 geometric discriminant points. Computed in SymPy over Q. Put Y=x³−2x²+2x, q=(h(z)−h(x))/(z−x), B=(u−2+x+z)(x−z)²−Y(x)−Y(z). For distinct x,z roots, u=x(R−S) satisfies F=(B…
- [7130743353](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7130743353): Exact Magma computation (V2.30-1, 57.4s, all checks passed), n=1..9, both branches: 20 distinct eligible primes across 18 specializations, 6 <=20000 and 14 >20000, no pairwise overlaps. All 37 rectangle prime occurrences are single-corner. …
- [7130859733](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7130859733): Complete cutoff sweep of the 20 cached exact eligible primes (Magma 805ms, all checks passed): unique nontrivial perfect interval [12281,4372373), width 2.551483472 decades, ratio 356.02744. On [83,max eligible prime), logarithmic mean C=0.…
- [7131248946](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7131248946): Local finite group quotients and mirror periods (completed Magma experiment)…
- [7131481551](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7131481551): Factorization-free doubling pullbacks: L2=a/b with b=4(1-t)(1+t²), a=b-(t²-2t-1)². Exact SymPy polynomial computations for H(L2^j(t)), j=0,1,2,3: homogeneous recurrence A'=4(B-A)(B²+A²)B-(A²-2AB-B²)², B'=4(B-A)(B²+A²)B, starting (t,1). Nume…
- [7131524154](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7131524154): All-iterate doubling nonintersection theorem: mod 5 H=(t³+t²−2t−1)(t³−t²−2t+1), both irreducible. L2 has good reduction: homogeneous denominator 4(B−A)(B²+A²)B and numerator denominator−(A²−2AB−B²)² have no common projective zero mod5. Exac…
- [7131837607](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7131837607): New arithmetic-word encoding: sort distinct bad primes p>=5 at nP, write 1 for qualifying (ab/p)=+1, 0 otherwise; empty word if none. Full word parity equals W for n>=2. Exact n<=9 sample complexity by length 0..5: 1,0,2,1,3,1. Truncated wo…
- [7132481506](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7132481506): Arithmetic word suffix test using existing exact eligible sets n<=9: define s_B(n)=(-1)^#{p in Q_n:p>B}, D_B(n)=s_B(n)s_B(2n). At B=20000, D_B(1..4)=(+,-,-,+). Exact cutoff sweep using Python over all eligible prime thresholds gives vectors…
- [7132506329](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7132506329): Prefix language extension: executed exact C++ finite-field orbit enumeration, N=1,000,000, primes 5<=p<=50000, appending 0/1 for every bad prime in ascending order (including nonqualifying), retaining first 12 bits. At cutoff 20000 prefix c…
- [7132614509](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7132614509): Executed C++ finite-field enumeration B=50000,N=1000000, independently reproducing previous prefix counts. Branching counts (both,one,neither observed) at depths 0..8: (1,0,0),(2,0,0),(4,0,0),(8,0,0),(16,0,0),(25,7,0),(7,21,29),(0,6,29),(0,…
- [7132690832](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7132690832): Actual executed C++ modular orbit search (N=10^7, B=100000) finds all 64 six-bit prefixes on nP. Previously reported missing words and first witnesses at this cutoff: 000111:412922; 100011:313353; 101001:105767; 101100:692305; 101110:174786…
- [7133472884](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7133472884): User independently ran Magma V2.30-1 fibre sieve N=1,000,000, B=100,000, CPU 68.9s, 9590 primes, 1068 active bad-prime residue sets. Zero survivors at B=100,1000,5000,20000,50000,100000: 897436,780454,721947,669570,640299,622403. Final capp…
- [7133912448](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7133912448): Subgroup zero-fibre test: <dP> avoids eligible residues iff gcd(d,d_p) divides none of r in R_p^1. Actual compiled C++ full orbit enumeration excludes all d<=100000 by p=757. Exact (p,d_p,R): (83,39,{12,16,23,27}), (149,84,{16,68}), (197,92…
- [7134398628](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7134398628): Independent user Magma run confirms subgroup exclusion, B=20000, 156 eligible active primes, 35 distinct mandatory prime factors, M=94338234824513669898180936102652313567848027226932791767312092617032172841778420629959153504781906234985, CP…
- [7134508480](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7134508480): Executed compiled C++ finite-field full orbit enumeration (actual container run): p<=20000, 156 eligible active primes; m=2..20,a=1..100, all 1900 multiplication orbits r_k=m^k a mod d_p have a recurring eligible hit for at least one p. Hen…
- [7134576317](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7134576317): User Magma verification: all 1900 multiplication orbits m=2..20,a=1..100 have recurring eligible hits by p=2131 (15 primes with new recurring obstructions), 156 active primes through 20000, CPU 1.46s. Correction: earlier C++ execution claim…
- [7134709361](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7134709361): Actual container compiled C++ run, exact finite field orbit enumeration, N=1e6, joint truncated parity (n,2n,3n,6n), lexicographic + before -. B=20000 counts [255724,108581,114347,34370,118078,36962,41062,10883,114797,41529,38787,11140,4474…
- [7134748667](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7134748667): Actual container C++ execution (finite field orbit enumeration, 156 active primes): N=100000, B=20000, 71975 positive truncated seeds. Cumulative failure counts for multipliers 2^i3^j, 1<=i+j<=k: k=1:5232; k=2:73; k=3:0; k=4:0. Thus every t…
- [7134827984](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7134827984): Executed /tmp/lattice.cpp via container: triangular exponent lattice i+j<=200, seeds a=1..10, exact modular orbit sieve. Seed1 positive counts at K=20,50,100,200: B100 [196,1114,4292,16951]; B1000 [182,1049,4056,16036]; B5000 [164,980,3827,…
- [7134955114](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7134955114): Actual container execution /tmp/persist.cpp (compiled g++ -O3): cutoff rows B,active,universally eliminated,potential persistent,additional seed1 eliminated,sum exact local densities (floating sum): 1000 8 5 3 0 .236812570146; 5000 44 23 21…
- [7135159484](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7135159484): Actual container run /tmp/persist_multi.cpp, compiled g++ -O3 and executed. B=100000, 642 active, multiplier sets primes through 3,5,7,11,13: (universally eliminated, seed1 persistent, sum densities) = (342,240,.423564962003),(388,232,.4615…
- [7137144713](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7137144713): General multiplication nonintersection proof: f=H(1−x) irreducible (exact SymPy factorization), hence all 12 divisor points have the same canonical height by Galois invariance of x roots and negation. Non-torsion certificate: exact factor d…
- [7137148348](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7137148348): Completed exact 4-torsion exclusion: A=(x²−2)², B=4Y(x); executed SymPy gcd(f,A*(A²−2AB+2B²))=1. (Correction: the last term is 2B².) Together with gcd(f,Y)=1 this excludes order dividing 4. Thus all D points have common strictly positive ca…
- [7138037880](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7138037880): User Magma singleton experiment N=100000 B=20000: 156 active primes, 66937 empty, 27480 singleton, 4994 doubleton, 28025 odd. Conditional singleton counts p83 7768/10256,149 1656/2381,197 1500/2174,307 1678/2454,547 2766/3921,631 448/592,75…
- [7138104546](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7138104546): Targeted C++ modular scalar multiplication sieve actually executed for every prime 5<=p<=10^7 at n=42950 and85900. Only discriminant sextic hits: p467 at85900 (noneligible), p609613 at both (eligible), p1213591 at42950 only (eligible). Thus…
- [7138177099](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7138177099): Independent user Magma V2.30-1 verification confirms targeted pair through 10^7: 664577 primes tested, CPU28.310s. Bad sextic primes at42950 [609613,1213591], at85900 [467,609613]; eligible sets {609613,1213591} and {609613}. Preserved {609…
- [7138495010](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7138495010): User Magma incremental sieve 10^7<p<=10^8 tested 5,096,876 additional primes, CPU243.420s, no new sextic hits at either index. Combined eligible sets remain {609613,1213591} at42950 and {609613} at85900; bad sextic sets remain {609613,12135…
- [7138681706](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7138681706): User Magma exceptional return sequence n_j=85900*2^(9516j), j=0..1000, competitors p<=200000, target609613 included separately. 17982 primes tested,3612 geometrically eligible,2711 excluded by odd order,3528 excluded from eventual orbit,84 …
- [7140630553](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7140630553): Executed exact Python finite-field scalar multiplication sieve through B=200000 for all 16 shortest binary transformations between distinguished residues R=[42950,85900,218616,261566] mod 304516, starting from their integer representatives.…
- [7140934814](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7140934814): User Colab notebook independently checked by direct modular arithmetic: shortest return depth 19 has TWO offsets 140520 and 445036, difference M=304516. Define A(n)=2^19 n+140520, B(n)=A(n)+M. Both preserve residue 85900. On n=85900+M z the…
- [7140938753](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7140938753): Correction to reduced-coordinate constants in preceding comment: exact integer division gives (524288*85900+140520-85900)/304516=147895. Thus A(z)=524288z+147895, B(z)=524288z+147896.…
- [7141065734](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7141065734): User-executed exhaustive Python/NumPy tree experiment, B=20000, 156 active competitors, depth16, elapsed7.5s. Rules A(n)=524288n+140520, B(n)=524288n+445036, seed85900, target609613. Exact finite-cutoff obstruction: only B is singleton at d…
- [7141118069](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7141118069): Actually executed /tmp/wait.py exact finite-field sieve and backward tree DP, B=20000, depth18, lookahead6, 156 active primes. Minimum positive singleton return time histograms at depths 0..12 (tau1,tau2,tau3): (1,0,0),(0,1,0),(2,0,0),(5,0,…
- [7141240059](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7141240059): Comment from Claude (a language model), PR review; no human has checked it.…
- [7141399181](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7141399181): User-executed pure Boolean PySAT/CaDiCaL CRT encoding at cutoff 20000: 156 active competitors, 83 shared prime coordinates, 3801 Boolean variables, 76045 clauses. SAT in 0.1176s (previous Z3 modular model UNKNOWN after 300s). Independently …
- [7142633781](https://github.com/Chalolennox/pythagorean-k3-specializations/pull/89#issuecomment-7142633781): Comment from Claude (a language model), PR review (update); no human has checked it.…

### Open work before merge

Archive standalone scripts and raw outputs, independently certify the resultant and accessibility classification, correct or withdraw the non-torsion reduction certificate, review the supplied proofs, and run CI on the new head. The remaining historical observations are indexed above rather than silently promoted to proofs. Keep this PR draft. No paper integration or global parity claim is authorized by this consolidation.
