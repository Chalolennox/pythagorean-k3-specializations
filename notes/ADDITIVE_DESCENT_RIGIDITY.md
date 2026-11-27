# Additive descent rigidity (25 November 2026)

Companion to PR #92. Proofs below are elementary or use the standard elliptic formal group; independent human review pending. No consequence for Problem H is claimed.

## 1. Primitive fourth-power decomposition

On J: y²=x³−2x²+2x, write x=m²/D² with positive coprime integers m,D, and l>0 with l²=m⁴−2m²D²+2D⁴. Put U=l−m²+D², V=l+m²−D². Both are positive and UV=D⁴, V−U=2(m²−D²), U+V=2l. An odd prime dividing both U,V would divide D and m, impossible. Thus their odd parts are coprime fourth powers. If D is odd, U,V are odd and U=r⁴,V=s⁴,D=rs. If D is even, m,l are odd, both factors even and v₂(V−U)=1, so their valuations are 1 and 4v₂(D)−1 in some order. In particular gcd(U,V)=gcd(2,D). Absorbing multiples of four in the exponents gives (U,V)=(8r⁴,2s⁴) or its swap, D=2rs. Here r,s are coprime but need not both be odd. Alternatively keep r,s odd and retain full powers of two; then rs is the odd part of D. The orbit orientation (3,1) modulo four was observed, not proved.

## 2. Sparse discriminant identities

Let N=D¹² H(1−m²/D²), H(t)=t⁶−30t⁴−24t²−1 (signed numerator, not absolute value). Put a=(m²−D²)²,b=D⁴. Then N=a³−30a²b−24ab²−b³ and a+b=l². Substitution proves
N=l⁶−33l⁴D⁴+39l²D⁸−8D¹².
Also 64N=(V−U)⁶−120(V−U)⁴UV−384(V−U)²(UV)²−64(UV)³
= U⁶−126U⁵V+111U⁴V²−36U³V³+111U²V⁴−126UV⁵+V⁶.
This corrects an earlier erroneous handwritten expansion. Substituting the fourth-power forms gives homogeneous degree-24 forms with the additional equation 2m²=2D²+V−U.

## 3. Multiplication linkage

Duplication gives sqrt(x(2Q))=±(m⁴−2D⁴)/(2mDl).
Triplication gives sqrt(x(3Q))=±(m⁹−12m⁵D⁴+16m³D⁶−12mD⁸)/(3m⁸D−8m⁶D³+12m⁴D⁵−4D⁹).
The latter follows by substituting x=m²/D² in the chord-formula triplication map and squaring the displayed ratio (owner Magma symbolic verification). Maps commute.

For Q=jP, write D_j for its reduced square-coordinate denominator. At any odd p dividing D_j, Q lies in the formal group. The formal logarithm is valuation preserving on pZ_p for odd p; hence v_p(D_kj)=v_p(D_j)+v_p(k). At 2, the duplication and odd-multiplication laws are already established in paper F.22. In particular D_j divides D_kj. For the odd fourth roots r_j,s_j, their product divides r_kj s_kj. Individual oriented propagation (doubling merges both into r, triplication preserves r,s) is only observed from gcd bit lengths, not proved; no exact individual divisibility assertion was run.

## 4. Denominator exclusion and sixth-power congruences

For every p|D, m is a unit and N≡m¹² mod p, so gcd(N,D)=1. Therefore gcd(N_kj,D_j)=1 for every k≥1. More precisely
N≡(m²−D²)⁶ mod D⁴.
The earlier claim N≡m¹² mod D⁴ was incorrect: the correct expansion is m¹²−6m¹⁰D² mod D⁴.
For p≥5 dividing D, N/(m²−D²)⁶ belongs to 1+p^(4v_p(D)) Z_p. Hensel's lemma (6 a unit) proves N is a sixth power in Q_p. Consequently all four signed numerators N_j,N_2j,N_3j,N_6j are sixth powers in Q_p for each p≥5 dividing D_j.

For p≡1 mod 6 in this set, factoring |N|=product q_i^e_i gives product (q_i/p)_6^e_i=(sign N/p)_6^(-1), with a fixed choice of sixth-power character. These are multiplicity-weighted constraints, not counts of distinct qualifying primes.

At a prime p≥5 dividing N, D is a unit; z=l²/D⁴ satisfies z³−33z²+39z−8=0, with z and z−1 squares modulo p. Also U/V is a scaled fourth power (both units since UV=D⁴). This is a necessary local condition, not a proof of accessibility or a new parity law.

## 5. Computation and scope

Owner-pasted Magma V2.30-1 output, seed 1778785146, 1.6s, 25 November 2026: symbolic identities, map degrees (4,3),(9,8),(36,35), commutation and rational triplication square root PASS. Eleven complete visible grids (44 vertex visits), seeds 1 through 11, all fourth-power decompositions, sparse identities and doubling/triplication edges PASS. Output truncated at start of seed 12; do not claim final summary or seed 12 completion. Observed gcd 1 for odd indices, 2 for even; even valuations (4v₂(D)−1,1) in displayed orientation. Cross-vertex gcd bit lengths suggest oriented propagation but are not exact divisibility certificates. No discriminant factorization performed.

## 6. Decision

Close the higher-power residue branch without further computation. The propagated primes are denominator primes, excluded from discriminant numerators. Residue characters constrain weighted products, not distinct qualifying-prime parity; the local cubic/fourth-power test would risk repeating accessibility research. Paper F.22/F.55 already cover denominator valuations/divisibility, F.52/F.56 quadratic reciprocity. No claim of novelty for those inputs. No exclusion of M15, no proof of infinitely many non-M15 original-orbit blocks, and no rank conclusion. Retain the identities and pursue only a mechanism linking joint parity of the four vertices. 
