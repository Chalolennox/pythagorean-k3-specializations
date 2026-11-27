# Symmetric cover label obstruction

For the selected sixteen primes and seeds n=72,360,504,2520, let a_n be the XOR of the local qualifying labels. On the symmetric cover L intersect SL, compare a_n(z) with a_n(Sz+t) for arbitrary integer translation t.

Theorem: their disagreement density is at least 2900/2105401, strictly positive, for every t. The same proof works comparing any two of the four seeds on a common cover.

Proof. At p=5779 the effective modulus is 2903 for all four seeds. The local quotient has order 1451 (prime), with 3=2^792 mod 2903. Each seed has a singleton qualifying support. In exponent coordinates the two support conditions are affine lines i+792j=c and 792i+j=c' modulo 1451. Their determinant 1-792^2 is 1020 modulo 1451, nonzero. Hence each line has density 1/1451 and their intersection density 1/1451^2, independently of translation and singleton positions. The local XOR has density D=2900/2105401 < 1/2.

Every other active local quotient for the four seeds has order coprime to 1451, as verified by enumerating the local orbits from the committed owner residues. Intersecting each lattice with its transpose gives an index dividing the square of its original index. The combined other-prime symmetric quotient therefore still has order coprime to 1451. The 5779 symmetric quotient is F_1451^2. The joint projection from the common cover onto these two quotients is surjective by coprime orders, so the uniform variables are independent. If the remaining XOR has density q, total disagreement is D+(1-2D)q >= D. This proves the claim, even after arbitrary translation.

The symmetric cover supports coordinate swap geometrically, and paired channels (a(z),a(Sz)) are exchanged. This does not preserve the original scalar label. For odd-index symmetric covers, adjoining the independent mod-4 coordinates gives the abstract order-32 reference action by CRT, but does not supply the missing original-label symmetry.

Verification: exact JavaScript orbit enumeration confirmed the singleton at 5779 and coprimality of all other active orders for all four seeds; 792^2 mod 1451=432. The earlier reported decimal disagreement values for individual seeds are not included as certified results because no execution record of the claimed exact Walsh calculation was available. The rigorous uniform lower bound suffices for the negative conclusion. Input residue data remain conditional on the owner Magma run. Scope: selected finite prime set, four seeds, coordinate swap with translation; not arbitrary arithmetic operations or the infinite-prime problem.
