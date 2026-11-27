# Further de Bruijn arithmetic realization obstructions

Companion to SYMMETRIC_COVER_LABEL_OBSTRUCTION.md. Human review pending.

## 1. Affine square symmetries

For seeds 72,360,504,2520 and the selected sixteen primes, use the isolated singleton component at p=5779, of order 1451, with row vector l=(1,792). For any M in GL_2(Z) and translation t, if det(l,lM) is nonzero modulo 1451, the original and transformed local singleton lines intersect in exactly one point of F_1451^2. On the joint common cover, all other local factors have order coprime to 1451, even after intersecting with their transformed lattices. Thus independence gives disagreement D+(1-2D)q, where D=2900/2105401 and 0<=q<=1. Both disagreement and agreement are at least D, so neither equality nor complemented equality is possible, including between different tested seeds.

Exact determinant residues for horizontal reflection, vertical reflection, transpose, anti-transpose, quarter rotation and inverse quarter rotation are respectively 133,1318,1020,431,1018,433 (with matrices diag(-1,1), diag(1,-1), swap, negative swap, [[0,-1],[1,0]], [[0,1],[-1,0]]). Identity and negative identity survive this necessary test, not necessarily all arithmetic tests. Neither exchanges the reference translation orbits. This does not exclude general affine matrices or CRT lifts.

## 2. Reference affine classification and its limitation

Exhaustive JavaScript enumeration of all 65536 binary arrays recovered 32 valid wrapped de Bruijn arrays, with 16 translates of the reference A. Among 96 invertible matrices mod 4, 32 preserve the valid set, 16 exchange the two translation orbits, and 12 of those are involutions. Including translations gives 512 preserving affine maps, 256 exchanging orbits. Each exchanging linear involution generates a distinct regular order-32 subgroup with translations. The other four exchanging matrices need not be involutions; no claim that these 12 exhaust all regular subgroups. The eight additional involutions beyond square symmetries are [[1,0],[2,1]], [[1,2],[0,1]], [[1,2],[2,3]], [[2,1],[1,2]], [[2,3],[3,2]], [[3,0],[2,3]], [[3,2],[0,3]], [[3,2],[2,1]].

For odd-index L, CRT identifies Z^2/(L intersect 4Z^2) with Z^2/L times (Z/4)^2. Acting only on the latter factor lifts all reference affine actions and preserves arithmetic labels, but introduces independent reference data; this is not intrinsic arithmetic extraction.

## 3. Intrinsic quotient obstruction

Any translation-equivariant map of configurations sends a period of its input to a period of its output. In particular any fixed finite-window Boolean rule has this property. Every valid wrapped 4x4 de Bruijn array has exact period lattice 4Z^2, since any nonzero period modulo 4 would repeat a tile code. Thus a necessary condition for extraction from a configuration with known period lattice L is L contained in 4Z^2 (and index divisible by 16). This does not require L to be the full stabilizer.

The prior active-lattice classification for the selected sixteen primes and n=72k gives image of L modulo 4 either C4 x C2 or C4 x C4. Neither is trivial. Consequently no such translation-equivariant extraction is possible for these finite-prime configurations, conditional on the input residue data and classification. For odd-order arithmetic quotient, every affine homomorphism from (Z/4)^2 into it is constant, so affine vertex selection also fails. Nonlinear selections and the complete parity function are not excluded.

## 4. Nonlinear recurrence obstruction (independent of prime cutoff)

On the auxiliary elliptic curve, R(Q)=Q+P, D(Q)=2Q, C(Q)=3Q, J_k(Q)=kP-Q. The recurrence of F.57 is R(t,u)=(u,(2u-4)/u^2-t) on its rational domain, extended via the elliptic curve. Exact identities DR=R^2D, CR=R^3C, DC=CD, J_k=R^k J_0 hold. Negation J_0 fixes the parameter 1-x(Q) and hence the complete multiplication parity block.

Suppose these operations descend to permutations of a common configuration set, respecting the identities, and the induced group has order 32 (or any power of 2). Then d r d^{-1}=r^2, so ord(r)=ord(r^2) forces ord(r) odd. Lagrange forces r=1. Likewise the tripling relation forces ord(r) coprime to 3 in any finite permutation quotient. Since j_0=1, every j_k=1. The remaining generators d,c commute, so cannot generate the nonabelian reference group (C4 x C4) semidirect C2. This is conditional on descent to permutations and group order; acting on 32 objects alone does not imply group order 32. An abelian regular action, noninvertible dynamics, other operations, and richer recurrence states remain outside the theorem.

Stronger if descent is required on all integer seeds: r=1 implies B_{n+1}=B_n for every n in the domain, so the block map is constant along the orbit; it cannot realize 32 distinct configurations. This conclusion does not apply to a subset not invariant under R.

## 5. Complete parity caveat

No finite-prime period obstruction automatically applies to the complete parity function. A valid 4x4 block at arbitrarily large positive seeds would imply infinitely many occurrences of both parity bits, but a single wrapped block does not establish arithmetic periodicity. The fair-coin probability 1/2048 is heuristic only. No complete-parity search or factorization was executed for this note.

Verification: modular determinants and reference affine enumeration executed in JavaScript; other statements are algebraic deductions. Prior residue inputs not independently recertified here. No consequence for Problem H is claimed.
