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
