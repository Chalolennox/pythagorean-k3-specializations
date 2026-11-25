# Geometric symmetric Sidon property of the discriminant divisor

Research note, 25 November 2026. AI-authored argument; owner supplied Magma execution transcript; independent human proof review pending. Follow-up to merged PR #89 and Problem H (#83).

## Theorem and certificate

Let J: y²=x³−2x²+2x and D={Q: h(x(Q))=0} over Qbar, where h=x^6−6x^5−15x^4+100x^3−189x²+162x−54. Then D consists of twelve points, is invariant under negation, and all unordered pair sums other than the six opposite pairs are nonzero and distinct (pairs allow repetition).

Proof: J has discriminant −256, so good reduction at 2621. The monic h is squarefree modulo 2621 and coprime to Y=x³−2x²+2x. Its six roots and both nonzero square roots of Y at each root are in F_2621. At any place over 2621 in a number field containing D, reduction gives a bijection of D onto these twelve points: integrality and simple roots ensure distinct reductions, including the two signs. Good reduction respects addition. The supplied Magma certificate enumerates all 78 unordered pairs and verifies exactly six zero sums and 72 distinct nonzero sums. The six opposite pairs already account for all zero sums. Thus every nonopposite pair has nonzero reduction and any equality between distinct nonopposite pairs in characteristic zero would contradict the certificate. This explicitly rules out the potential issue of a nonzero sum reducing to zero.

## Translation consequence

For R nonzero, ordered representations Q−S=R correspond to unordered representations Q+(-S)=R. Each unordered pair contributes two ordered representations if its entries differ and one if equal. Thus |D intersect (D+R)| <= 2. Exactly 12 translations have multiplicity one (doubles), 60 have multiplicity two (distinct nonopposite pairs), and the identity has multiplicity 12. All other translations have multiplicity zero. Check: 12+12+120=144.

## Arithmetic scope and open work

Only finitely many rational primes can spoil this property: in a fixed number field containing the points and sums, exclude bad reduction, collisions among D, and places where distinct sums coincide or a nonopposite sum reduces to O. Distinct sections coincide at only finitely many places (equivalently their nonzero difference reduces to O at finitely many places). Outside these primes the bound holds geometrically, hence for the eligible subset D_p^+ and its orbit-accessible subset. An explicit exhaustive exceptional-prime classification is pending. No claim that the theorem proves singleton survival or Problem H; distinct competitors can still enter at successive indices. Earlier three-way exclusions alone do not imply this four-point property. The abstract two-element symmetric support countermodel remains an obstruction to deducing global parity from these constraints alone.

## Reproduction

- [Magma script](../code/magma/geometric_sidon_certificate.m): standalone script supplied in chat, whitespace compacted without changing statements.
- [Raw owner output](data/geometric_sidon_20261125.txt): verbatim pasted transcript including timing, version, memory and seed. Owner reported PASS on 25 November 2026. Not a connector-side Magma execution; no independent human review claimed.


## Explicit arithmetic classification (25 November 2026)

Put Y=x^3-2x^2+2x, H(t)=h(1-t), g(t)=2t(1-t^2). Let D_p be the rational points with h(x)=0, D_p^+ those with g(1-x) a nonzero square, and S_p=D_p^+ intersect <P mod p>, P=(1,1).

**Theorem (computational certificate, independent review pending).** For every p>=5 and nonidentity R in J(F_p), |S_p intersect (S_p+R)|<=2. For D_p^+ the same holds except p=519521, R=T=(0,0), where the intersection has size 4. For D_p the universal bound is 4.

### Exhaustiveness argument

Use u for the x-coordinate of a sum. Doubling gives L6=Res_x(h(x),4uY(x)-(x^2-2)^2). For distinct coordinates x,z, put q=(h(z)-h(x))/(z-x), B=(u-2+x+z)(x-z)^2-Y(x)-Y(z), F=(B^2-4Y(x)Y(z))/(x-z)^2. The latter is polynomial by direct substitution and expansion. Compute Res_x(h, Res_z(q,F) mod h), of degree 60; its primitive square root is L30. The primitive product L36=L6 L30 has degree 36 and is squarefree. Outside 2,3,23 the six roots of h are distinct, Y is nonzero there, and all denominators in the monic pair-sum polynomial are units: they come from 4Y(x) and (x-z)^2. Thus reduction preserves the 36 indexed x-coordinates of nonopposite pair sums, counting each sum and its negative once. The resultant formula follows by multiplying over the six roots and the five other roots for each, with each unordered coordinate pair counted twice. Opposite pairs remain opposite and all other sums remain finite by the addition and doubling formulas. Excluding primes dividing the leading coefficient, discriminant of L36 and Res(L36,Y) ensures these indexed coordinates remain distinct and none is a 2-torsion coordinate. Hence distinct unordered nonopposite pairs cannot have equal sums, and ordered difference multiplicity is at most two. This proves exhaustiveness, not that every candidate is exceptional.

The owner ran the decomposition into irreducible factors of degrees 6,6,24. The discriminant identity disc(L36)=product disc(fi) times product Res(fi,fj)^2 passed. Trial division, perfect-power removal and shared-gcd splitting reduced the 5596-bit discriminant problem to seven residuals of 18,48,66,131,210,238,241 bits. All eleven certificates were completely supported on the recovered primes, with primality assertions. CPU 8.100 s, Magma V2.30-1 seed 1778881808.

Candidate primes (33):
5, 7, 19, 23, 41, 83, 97, 103, 113, 157, 257, 4583, 55009, 64811, 70297, 96001, 103967, 138679, 248389, 519521, 609571, 43185607, 254717627, 280937621, 990716219, 7170845597, 30358338574451, 45886915050671, 1531941337378691479, 344440033300531101843589, 12171150351860362096713064958322911, 1203273355205525581931059818759348924273956480384606123, 5136714670616930401674408573902323936996380257286318245563.

### Exact rational classification

For each candidate enumerate roots of h in F_p and both rational square roots of Y, filter by g, then count all nonidentity ordered differences. The owner output was split and truncated during candidate 33; a separate final-candidate run completed it (seed 1778882324). Rational exceptions and maxima (D_p,D_p^+):

| p | D_p | D_p^+ |
|---|---:|---:|
|83|3|2|
|55009|3|0|
|64811|4|2|
|103967|4|1|
|138679|3|1|
|519521|4|4|
|609571|4|2|
|43185607|4|2|
|254717627|4|2|
|5136714670616930401674408573902323936996380257286318245563|4|2|

All other candidates have maxima <=2. The sole eligible violating shift is T at 519521. This is a prime-field classification, not a classification over algebraic closures at exceptional primes.

At 519521 the owner found #J=519312, ord(P)=698, T in <P>, eight eligible points and zero accessible eligible points. Full T-intersection=4, orbit T-intersection=0, maximum orbit intersection=0 (Magma V2.30-1 seed 1778882407). Thus the orbit bound has no exceptions. The eight eligible points have x-coordinates 37492,134940,384583,482031 with respective positive listed y-coordinates 211910,252079,144950,230963 and their negatives.

### Consequences and limitations

For d_p=ord(P mod p), any k not divisible by d_p has at most two residues n mod d_p with both nP and (n+k)P eligible. If n,n+a,n+b,n+a+b are all eligible and a is nonzero modulo d_p, the two witnesses for difference aP either coincide or are exchanged by (A,B)->(-B,-A), because the set is symmetric and the multiplicity is <=2. Therefore b=0 or 2n+a+b=0 modulo d_p. No conclusion when a=0 modulo d_p.

This is a uniform local constraint, not a proof of global parity variation or singleton survival. The earlier abstract symmetric two-element support countermodel still applies. No independent Magma execution or human review claimed. The preceding historical section describes the earlier state, superseded by this update. The original raw-output description above should be read cautiously: the archived initial certificate transcript was reconstructed from the chat result, not independently verified verbatim.
