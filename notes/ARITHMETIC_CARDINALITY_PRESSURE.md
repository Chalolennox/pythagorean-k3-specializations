# Arithmetic cardinality pressure: a rigorous limitation of the relaxed graph model

25 November 2026. Companion to GEOMETRIC_SIDON.md and MULTIPLICATION_GRAPH_RELATIONS.md, PR #92. AI-derived proof, human review pending.

## Definitions and finite experiment

For a finite graph G with edge-specific allowed intersections, let T_B be the signed ordered primitive nondegenerate Pythagorean triples of hypotenuse <= B. Put F=4a^3+27b^2c and Q(T)={p>=5: p|F and (ab/p)=1}. An assignment is injective and satisfies every edge restriction. Its bottleneck is the minimum |Q(T)|. Define M_B(G) as the maximum bottleneck over feasible assignments and M_B(G_0) for the same vertices without edges. Define pressure Pi_B(G)=M_B(G_0)-M_B(G), only when feasible. Superscript odd restricts all candidates to odd cardinalities. Both capacities are nondecreasing in B when defined; their difference need not be. Pressure is nonnegative and nondecreasing under adding constraints at fixed B and vertex set. Infeasibility is a separate status. The liminf of pressure (where eventually defined) is one possible asymptotic invariant; unbounded capacity does not settle it.

Owner computation at B=1000: 1264 triples, cardinality histogram 0:349, 1:578, 2:289, 3:43, 4:5. A 3x3 odd grid achieved threshold 3 (control 3). At 6x6, control 3, 43 threshold-3 candidates, Boolean SAT encoding 4565 variables and 84711 clauses, timeout 600.102 seconds, UNKNOWN. No gap certified. These are summaries of owner-reported outputs, not independent executions. The horizontal, vertical, cross and forward diagonal rules of PR #92 all permit empty intersections. The relaxed game does not require multiplication linkage.

## Arithmetic normalization

Write H(t)=t^6-30t^4-24t^2-1, G(t)=2t(1-t^2), and D(u,v)=v^6 H(u/v). For coprime u,v, take (a,b,c)=(v^2-u^2,2uv,u^2+v^2)/d with d the gcd (1 or 2). Then F=-4D/d^3 and ab=2uv(v^2-u^2)/d^2. At p>=5 dividing D, v is a unit (otherwise u is a unit and D=u^6 mod p); thus eligibility is exactly (G(u/v)/p)=1. Neither 0 nor +/-1 is a root mod p>=5 since H(0)=-1 and H(+/-1)=-54. In particular the character is never zero at these roots. H is separable: H'=6t(t^4-20t^2-8); H(0)=-1, and the cubic z^3-30z^2-24z-1 has no common root with its derivative (division leaves -216z-81, whose root -3/8 does not satisfy z^2-20z-8=0). Thus D has no repeated factor and no root at infinity.

## Proposition 1: CRT inclusion and avoidance

For any finite prime set S and r>=1 there are infinitely many integer parameters t with |Q(t)|>=r and Q(t) disjoint from S. Indeed choose an algebraic root alpha of H. G(alpha) is nonzero. In the normal closure of Q(alpha,sqrt(G(alpha)),i), completely split primes have positive Chebotarev density. Excluding finitely many primes (including 2,3, discriminant and denominators), they are 1 mod 4 and admit simple roots alpha_p of H with G(alpha_p) a nonzero square. Choose r distinct such primes outside S. CRT prescribes t=alpha_p modulo each chosen prime and t=0 modulo every q>=5 in S. The latter excludes q because H(0)=-1. Arbitrarily large positive solutions yield distinct triples. This already gives unbounded capacity without parity, and induction gives pairwise disjoint eligible sets by forbidding the finite union of previous sets.

## Proposition 2: reflection

H is even and G is odd. Hence for every rational parameter t with primitive coordinates,
s(t)+s(-t) = #{p>=5:p|D(u,v), p=3 mod 4} (mod 2),
where s(t)=|Q(t)|. Primes 1 mod 4 contribute twice or zero, and primes 3 mod 4 contribute exactly once. If D>0 is squarefree and D=3 mod 4 with gcd(D,6)=1, the right side is odd. This does not assert that even valuations are impossible in general. For integer t, the corresponding squarefree-value step is not established here; the rational two-variable construction below removes that obstruction.

## Theorem: arbitrarily many odd eligible primes with arbitrary finite avoidance

For every finite forbidden prime set S and every integer r>=1, infinitely many rational parameters t satisfy Q(t) disjoint from S, |Q(t)|>=r and |Q(t)| odd.

Proof. Choose r good split primes p_i as above. For each choose a lift beta_i modulo p_i^2 of its eligible root such that H(beta_i) is divisible by p_i but not p_i^2. The simple-root condition guarantees such a lift. Impose on (u,v) the CRT conditions
- (u,v)=(beta_i,1) mod p_i^2;
- (u,v)=(0,1) mod q for q>=5 in S;
- (u,v)=(0,1) mod 6.

Let M be the product of these pairwise coprime moduli. The residue class has no fixed square divisor of D: at p_i valuation is exactly one; at other primes dividing M the value is a unit; at any prime ell not dividing M we can additionally prescribe (u,v)=(0,1) mod ell^2, giving D=-1 mod ell^2.

Apply Greaves's squarefree binary-form theorem in the congruence and region version of Lemke Oliver and Thorne, Lemma 6.2 (references below). Every irreducible factor of D has degree <=6 and D is separable. Choose a smooth positive-area domain Omega contained in 0<v<u/6, u<1. On this domain D>0: for t>6, H=t^4(t^2-30)-24t^2-1>0 since t^2>36. The lemma gives a positive leading constant times X^2 squarefree values counted by pairs in X Omega in the fixed CRT class, with error O(X^2/(log X)^(1/3)). In particular infinitely many such pairs exist. Squarefreeness forces gcd(u,v)=1 by homogeneity, and v>0 gives unique reduced parameters. The imposed 2-adic parity gives d=1; D=3 mod 4, and the modulo 3 condition gives D=-1 mod 3. So D is positive squarefree and coprime to 6.

Both t=u/v and -t have the r prescribed eligible primes (all p_i=1 mod 4) and avoid S. By Proposition 2 exactly one has odd eligible cardinality. Selecting that sign yields infinitely many distinct rational parameters, since each absolute parameter has at most two signs. QED.

## Corollaries and scope

For any fixed finite graph whose edge rules allow disjoint sets, and any r>=1, choose triples inductively by the theorem, taking S to be the complete union of prime sets at previous vertices. Every new set is odd, has size at least r, and is disjoint from all earlier sets. Distinctness follows from nonempty disjoint sets; heights can additionally be chosen strictly increasing because each step has infinitely many solutions and finitely many bounded-height triples. Thus sup_B M_B^odd(G)=infinity, also for the unrestricted capacity. The same induction constructs countably infinite all-odd assignments, with arbitrary prescribed lower cardinality bounds at individual vertices. In particular no absolute odd-parity obstruction follows from these edge restrictions in the relaxed model, even when every vertex is a genuine primitive Pythagorean triple. This does not prove that finite-height pressure tends to zero, or that the integer-parameter version with odd parity holds.

Crucially this does NOT give a grid of the form t(n*2^i*3^j P), nor settle Problem H. The proof uses unrestricted independent rational parameters; Greaves's two-variable count does not apply to the thin elliptic orbit. An obstruction for the actual multiplication grid must use additional linkage information. No claim about rank or root-number parity on that orbit follows.

## References

- G. Greaves, Power-Free Values of Binary Forms, Q. J. Math. 43 (1992), 45–65.
- R. J. Lemke Oliver and F. Thorne, Rank Growth of Elliptic Curves in Non-Abelian Extensions, IMRN 2021, 18411–18462, specifically Lemma 6.2: https://academic.oup.com/imrn/article/2021/24/18411/5673238 . The congruence/region statement and its proof were consulted directly for this note.
- Canonical paper, F.51–F.57 for normalization and qualifying primes; PR #92 companion notes for multiplication constraints.

No novelty claim for max-min optimization or multicoloring. The specific arithmetic theorem is a deduction from published squarefree sieve and Chebotarev results, not a new sieve theorem.
