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

The owner ran the decomposition into irreducible factors of degrees 6,6,24. The discriminant identity disc(L36)=product disc(fi) times product Res(fi,fj)^2 passed. Trial division, perfect-power removal and shared-gcd splitting reduced the 5596-bit discriminant problem to seven residuals. All twelve certificates were completely supported on the recovered primes, with primality assertions. CPU 8.100 s, Magma V2.30-1 seed 1778881808.

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

For d_p=ord(P mod p), any k not divisible by d_p has at most two residues n mod d_p with both nP and (n+k)P eligible. If n,n+a,n+b,n+a+b are all eligible and a is nonzero modulo d_p, the two witnesses for difference aP either coincide, are exchanged by (A,B)->(-B,-A), or are both fixed by this involution. Therefore b=0, or 2n+a+b=0, or both 2n+a=0 and 2b=0 modulo d_p. The last possibility was omitted in the earlier formulation. No conclusion when a=0 modulo d_p.

This is a uniform local constraint, not a proof of global parity variation or singleton survival. The earlier abstract symmetric two-element support countermodel still applies. No independent Magma execution or human review claimed. The preceding historical section describes the earlier state, superseded by this update. The original raw-output description above should be read cautiously: the archived initial certificate transcript was reconstructed from the chat result, not independently verified verbatim.


## Multiplication square and order-four exclusion (25 November 2026)

Status: proof given conditional on the orbit Sidon and earlier three-way certificates; new finite computations Observed in owner Magma runs, human review pending.

### No nondegenerate three-term progression

If n,n+k,n+2k are distinct qualifying residues, the two difference-k witnesses cannot coincide. If exchanged under negation, the middle point is 2-torsion; if both fixed, 2k=0, contradicting distinctness. Both are impossible: Res(h,Y) has absolute value 3456=2^7*3^3. Thus no nondegenerate three-term progression occurs. In particular Q(n) intersect Q(2n) intersect Q(3n) is empty. Here Q(n) denotes the complete qualifying prime set, not a truncated sieve.

### Order four and tripling

The reduced fourth division polynomial is (x^2-2)(x^4-4x^3+12x^2-8x+4). With N=(x^2-2)^2 and D=4Y, N^2-2ND+2D^2 equals the square of the quartic. Absolute resultants with h are 5768=2^3*7*103 and 1579024448=2^6*257*96001. Hence only four candidate primes >=5. Owner Magma PASS (V2.30-1, seed 1778882739, CPU 0.09 s):

|p|common x|#J|ord(P)|rational order-four points|eligible|
|---:|---:|---:|---:|---:|---:|
|7|4|12|6|0|0|
|103|38|108|54|0|0|
|257|112|240|30|2|2|
|96001|56138|96496|12062|2|0|

All orders are 2 mod 4, so no order-four point is accessible. If n and 3n qualify, symmetry gives the progression -n,n,3n. Distinct residues are impossible by the progression theorem; degeneracy forces 2nP=O or 4nP=O, also impossible. Thus Q(n) intersect Q(3n) is empty for all n. Earlier three-way classification gives Q(n) intersect Q(2n) contained in {609613}.

### Multiplication maps and diagonals

Let HomH(U,V)=V^6 h(U/V). N2=(x^2-2)^2, D2=4Y, psi3=3x^4-8x^3+12x^2-4, F4=(x^2-2)(x^4-4x^3+12x^2-8x+4), N3=x psi3^2-8Y F4, D3=psi3^2. Compose homogeneous degree-nine maps with (N2,D2) to obtain N6,D6. Write Hk=HomH(Nk,Dk). Owner verified multiplication maps and degrees 24,54,216, gcd(H2,H3)=gcd(h,H6)=1 over Q, so both characteristic-zero intersections are empty. Any rational finite-field witness forces the corresponding resultant to vanish modulo p; actual point multiplication and eligibility are checked after root enumeration, so spurious roots cannot certify exceptions.

First run timed out factoring R16 (seed 1778883455, 299.7 s). Staged run (seed 2499372010, CPU 0.210 s) completed R23 classification. R23 has 1727 bits, exponent of 2 is 1260, no factor 3. Remaining factors, all exponent one and primality checked:
19,23,1303,1747,33403,195787,109386611,11638358449,129482728939,10068739268579,8251484925099743,2604392352531386543367092980450490236218679289577269234343297013.

Every common polynomial has degree one. All primes except 109386611 and 11638358449 have zero eligible witnesses. At 11638358449 the two witnesses (2119117229,1308573334) and its negative are inaccessible (ord(P)=727400674). At 109386611, ord(P)=54701375, witnesses (83192951,24702877) and its negative have verified logs 21880550 and 32820825. No pending primes. Therefore Q(2n) intersect Q(3n) is contained in {109386611}, attained precisely at those residues for this prime.

R16 has 1716 bits, exponent of 2 is 324, no factor 3. Known odd factors: 19,23^2,313,1303,3931,109386611,129482728939. Remaining composite (1285 bits):
```
448950437226809926672528009325259643134351198363614585760251444427541089591531250618863854087792248939056144640495087710790873934189343652417741036374390411993778030206582588063177274526599298820431179361525555563153745362582421431355868738919088753359648448461029346324940042045177161221002242857907895227209162792493560502771199945316561222170968663333112702726707183543542556668504289
```
All seven known primes checked; only 109386611 has eligible accessible witnesses, (3016047,39605448) and its negative, logs 10940275 and 43761100. R16 classification is INCOMPLETE, not an exhaustive exception theorem. Defer unrestricted factorization.

At p=109386611 put r=10940275=d_p/5. On the order-five subgroup exactly +/-r qualify: these qualify by R16 witnesses, +/-2r cannot qualify by tripling exclusion (3r=-2r), and O is excluded. Multiplication-square patterns at +/-r are (1,0,0,1), at +/-2r (0,1,1,0), ordered n,2n,3n,6n.

|Pair|Possible common primes|
|---|---|
|n,2n|609613 only|
|n,3n|none|
|2n,6n|none|
|3n,6n|609613 only|
|2n,3n|109386611 only|
|n,6n|109386611 confirmed; other primes unresolved|

No prime occupies three vertices because the two tripling edges are disjoint and cover all four vertices. Hence the union cardinality is at least half the sum of the four cardinalities. This does not imply an empty vertex: disjoint singleton sets are compatible. Infinitely many complete empty Q(n) would imply H (positive root number, rank conclusion conditional on rank parity and known section). Fixed-cutoff emptiness follows by periodicity but does not imply complete emptiness. No global parity or singleton theorem claimed.

Execution provenance: the above is a summary of owner-pasted output, not an independently executed Magma certificate or verbatim raw log. Earlier assistant claims of Python execution are not relied upon. The original scripts and full raw logs still need separate archival. 
