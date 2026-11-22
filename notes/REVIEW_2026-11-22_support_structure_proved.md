# Support structure of the qualifying indices: what is proved, what is observed, what is open

Status: derived with a language model, 22 November 2026; no human has checked it. No consequence for Problem H; the paper is not changed. Code: code/verify_support_structure.py (standard library only; about 8 seconds), code/search_support_twelve.py (about 6 minutes to 3·10^7, not in CI), code/support_density_sum.py (about 35 s; not in CI). Data: data/support_twelve_search_3e7.txt, data/support_sum_30000.txt.

Labels. The claims policy in CONTRIBUTING.md reserves "Proved" for a proof that a human has read. Nothing below has been read by a human, so "Proof given" means: a complete proof is written out in this note, derived with a language model and not yet read by anyone; where a statement is finite it is also checked by the code. "Observed" is a finite computation with its limits stated. The standard facts about 2-descent are cited, not re-proved.

Origin. The questions come from the prime-synchronization dossier (an independent review that is not in the repo), from follow-up discussion with the owner (who supplied the proofs of Propositions 1 and 2 in outline), and from a reviewer's reply of 22 November 2026 (not in the repo) that states Proposition 8 and the root-level form of Proposition 6. The proofs below were written out and checked here, and may differ in detail from what was supplied.

## Definitions
C: y^2 = x^3 - 2x^2 + 2x, P = (1,1), T = (0,0), t(Q) = 1 - x(Q), H(t) = t^6 - 30t^4 - 24t^2 - 1 = C3(t^2) with C3(s) = s^3 - 30s^2 - 24s - 1, g(t) = 2t(1 - t^2). For a prime p >= 5 let m_p be the order of P in C(F_p), chi the Legendre symbol, and for j = 0, 1

- N_{p,j} = { n mod m_p : Q = nP + jT is affine and H(t(Q)) = 0 in F_p },
- S_{p,j} = { n in N_{p,j} : g(t(Q)) is a nonzero square mod p } (the qualifying indices).

S_{p,0} is the set S_p of notes/REVIEW_2026-11-19_support_two.md. Let R_p be the set of roots of H in F_p. Since H is even and H(0) = -1, R_p is a union of pairs {t, -t} with t != -t.

## Where this overlaps the repo
Already in the repo: the splitting field N of H with Gal(N/Q) = S_4 of order 24, proved in paper/paper.md (Appendix E, item 5 above Proposition E, near line 853) by the same relation y1 y2 y3 = 1 that Proposition 1 uses; the statement that x(nP) is a square (the paper, near line 584); and the 2-isogeny, the descent map delta and the even index [C(F_p) : <P>] in notes/REVIEW_2026-11-19_support_two.md. I did not find, by text search of paper/paper.md and notes/, a statement of the root-count law 0/2/6, the evenness of |N| and |S|, the bound by p mod 4, the necessary congruences for |S| = 12, the parity law, or the example below.

## Proposition 1 (root counts 0, 2, 6). Proof given; checked for every prime below 60000
For every prime p >= 5, #R_p is 0, 2 or 6.

Proof. C3 has discriminant 3^9 * 23. For p != 23, C3 is separable mod p and has 0, 1 or 3 roots in F_p. The roots of H are the t with t^2 = s, s a root of C3 (s = 0 is not a root, C3(0) = -1). A root s in F_p gives 1 + chi(s) roots t. If C3 has no root, #R_p = 0. If it has exactly one root s1, #R_p = 1 + chi(s1) in {0, 2}. If it has three roots s1, s2, s3 in F_p, then s1 s2 s3 = 1 (the constant term of C3 is -1), so chi(s1) chi(s2) chi(s3) = 1 and the number of non-squares among them is even; #R_p = 3 + sum chi(s_i) is 6 (none) or 2 (two non-squares). For p = 23, C3 has a double root and the count is 2 (computed; roots 5 and 18). []

Group-theoretic form. Since s1 s2 s3 = 1, the product of the three square roots a_i = sqrt(s_i) is +-1, and the Galois group of the splitting field of H lies in { (sigma, eps) : sigma in S_3, eps in {+-1}^3, eps_1 eps_2 eps_3 = 1 }, of order 24 (the paper proves that it has order 24, so it is this whole group). An element fixes the roots +-a_i for exactly those i with sigma(i) = i and eps_i = +1, so it fixes 6, 2 or 0 roots; the multiplicities are 1, 9, 14 (checked in the code). By Chebotarev the densities are the densities 14/24, 9/24, 1/24 for 0, 2, 6 roots. Observed over the 6055 primes 5 <= p <= 60000: 3557, 2262, 236, that is 0.587, 0.374, 0.039, against 0.583, 0.375, 0.042.

## Proposition 2 (evenness). Proof given; checked below 4000
For p >= 5 and j = 0, 1 the sets N_{p,j} and S_{p,j} are invariant under n -> -n and have even cardinality.

Proof. x(-Q) = x(Q), and -(nP + jT) = (-n)P + jT because 2T = O. Hence the condition on n depends only on x(Q) and the set is symmetric. A fixed index has 2n = 0, so Q = nP + jT satisfies 2Q = O: Q is a 2-torsion point of C(F_p), and it is affine only if Q = T or Q = (1 +- i, 0), the latter when p = 1 mod 4. For Q = T, t = 1 and H(1) = -54; for Q = (1 +- i, 0), t = -+i and H(+-i) = -8. Neither vanishes modulo p >= 5. So no fixed index lies in N_{p,j}, and N_{p,j} splits into pairs {n, -n} with n != -n; S is a subset closed under the same involution. []

## Proposition 3 (bounds by p mod 4). Proof given; checked below 4000
|S_{p,j}| <= 2 #R_p when p = 1 mod 4 and |S_{p,j}| <= #R_p when p = 3 mod 4. So the largest possible values are: p = 3 mod 4: 2 (two roots), 6 (six roots); p = 1 mod 4: 4 (two roots), 12 (six roots).

Proof. A root t comes from at most two indices (Q and -Q: n and -n, since n -> nP + jT is injective and x determines Q up to sign). If p = 3 mod 4 then chi(-1) = -1 and g(-t) = -g(t), so for each pair {t, -t} at most one of the two roots can have g(t) a nonzero square (g(t) != 0 on R_p as H(0), H(+-1) != 0). So at most #R_p/2 roots qualify and |S| <= #R_p. If p = 1 mod 4 every root can qualify. []

The unconditional bound |S_{p,j}| <= 12 was already clear; the new content is the dependence on p mod 4 and on #R_p. The earlier conjecture |S_{p,0}| <= 4 is false (see Observed).

## Proposition 4 (necessary congruences for |S| = 12, and the bound 12 is attained). Proof given; example checked with the original definition
(a) If |S_{p,0}| = 12 then p = 1 mod 24. (b) If |S_{p,1}| = 12 then p = 1 or 5 mod 24. (c) The prime p = 5251537 (= 1 mod 24) has |S_{p,1}| = 12, with m_p = 1313021, T not in <P>, and indices 57977, 139058, 159969, 410262, 462126, 519517, 793504, 850895, 902759, 1153052, 1173963, 1255044. So the bound in Proposition 3 is sharp.

Proof of (a), (b). By Proposition 3, |S| = 12 forces p = 1 mod 4, #R_p = 6, and all six roots t occur as t(Q) for some Q in the coset nP + jT with g(t) a square. On the curve, y^2 = x(x^2 - 2x + 2) = x(1 + t^2) for x = 1 - t, and y != 0 (the point is not 2-torsion). The six roots are +-a_i with s_i = a_i^2 the roots of C3, and prod(1 - s_i) = C3(1) = -54, prod(1 + s_i) = -C3(-1) = 8.

Branch 0. By Proposition 5 each x = 1 - t is a square; hence so are 1 + t^2 (from y^2) and (1 - t)(1 + t) = 1 - s. All 1 + s_i and 1 - s_i are squares, so 8 and -54 are squares: chi(2) = 1 and chi(-6) = 1, so chi(6) = 1 (chi(-1) = 1) and chi(3) = 1. Then p = 1 mod 8 and p = +-1 mod 12, so p = 1 mod 24.

Branch 1. Now x(Q) = 2/x' with x' a square, so chi(x(Q)) = chi(2), hence chi(1 - t) = chi(2) and chi(1 + t^2) = chi(2) for all six roots. Then 1 - s_i = (1 - t)(1 + t) is a square and -54 is a square, so chi(6) = 1. With chi(2) chi(3) = 1: if p = 1 mod 8 then chi(3) = 1 and p = 1 mod 24; if p = 5 mod 8 then chi(2) = -1, chi(3) = -1, p = 5 mod 12 and p = 5 mod 24. []

(c) is a computation: code/verify_support_structure.py walks the orbit of P modulo p with the full group law, adds T explicitly, and counts the indices with H(t) = 0 (12 of them, all with g(t) a square), and code/search_support_twelve.py found it. It is the only example below 3·10^7 (Observed, below). The congruence conditions are necessary, not sufficient: they do not decide that the six x-values lie in the coset.

## Proposition 5 (2-descent facts used). Standard; cited
(i) For a curve y^2 = x(x^2 + ax + b) the map Q -> x(Q) mod squares, T -> b, is a homomorphism C(K) -> K^*/K^*2 (Silverman, AEC X.4). Here b = 2 and x(P) = 1, so x(nP) is a nonzero square for every nP not in {O, T}, and x(nP + T) = 2/x(nP) has the class of 2. (ii) For Q = (x, y) one has x(Q + T) = 2/x(Q) (translation by (0,0) on this model; checked by the group law for p < 200). (iii) When p = 1 mod 4, with i^2 = -1, C(F_p) contains all of C[2] and the map delta(Q) = (x, x - (1 + i), x - (1 - i)) mod squares, with the usual replacement of the coordinate at a 2-torsion point, is a homomorphism with kernel 2C(F_p) (the connecting map of the 2-descent over a finite field).

## Proposition 6 (parity law for p = 5 mod 8). Proof given, from Proposition 5; checked for all points, p < 4000
Let p = 5 mod 8 and let i be a square root of -1 in F_p. Then:

(a) i is a non-square, and m_p is even.
(b) For every n with nP not 2-torsion, with t = t(nP): (-1)^n = chi(t + i).
(c) For every n with nP + T not 2-torsion, with t = t(nP + T): (-1)^n = chi(t + i) chi(-(1 + i)).
(d) For p = 1 mod 4 (any p): if n is even then chi(t + i) = 1 in (b), and chi(t + i) chi(-(1 + i)) = 1 in (c). The converse fails for p = 1 mod 8.

Proof. i^((p-1)/2) = (i^2)^((p-1)/4) = (-1)^((p-1)/4) = -1 as (p-1)/4 is odd, so i is a non-square, and chi(-1) = 1. By (iii), delta(P) = (1, -i, i), whose second coordinate is a non-square: delta(P) != 0, so P is not in 2C(F_p) and m_p is even (an odd m would give P = 2((m+1)/2)P). If n is even, nP is in 2C(F_p) and delta(nP) = 0, so chi(x - (1 + i)) = 1; if n is odd, delta(nP) = delta(P) and chi(x - (1 + i)) = chi(-i) = -1. Now x - (1 + i) = -(t + i) and chi(-1) = 1, so (-1)^n = chi(t + i). For (c), delta(T) = (2, -(1 + i), -(1 - i)) adds the factor chi(-(1 + i)) to the second coordinate. (d): the direction "n even => 1" uses only delta(nP) = 0 and holds for every p = 1 mod 4; for p = 1 mod 8, i is a square, delta(P) = 0 and the character does not determine the parity (p = 17 gives odd n with chi(t + i) = 1; checked). []

Remarks. (1) The hypothesis H(t) = 0 plays no role: the law holds at every point nP, not only at the qualifying ones, so it is a statement about the group, not about the sextic. In particular the reviewer's formulation (-1)^n = chi(r + i) for a root r with Q in <P>, t(Q) = r, is the special case t = r. (2) It reads the parity of n from one character, without walking the orbit. (3) For p = 3 mod 4 there is no i and no second descent: the parity is not read off in this way. (4) For p = 1 mod 8 it is not determined.

## Proposition 7 (the pair +-t on one branch). Proof given; checked on all pairs of this kind below the limit of the code (14236 pairs below 2000)
Let p = 5 mod 8, and suppose that t and -t both occur as t(Q), Q = nP + jT, Q' = n'P + jT (same branch j). If j = 0 then n and n' have the same parity; if j = 1 they have opposite parity.

Proof. By Proposition 6, (-1)^(n + n') = chi((t + i)(-t + i)) = chi(-(1 + t^2)) = chi(1 + t^2) for j = 0, and the factor chi(-(1 + i))^2 = 1 drops out for j = 1 too. On the curve y^2 = x(1 + t^2) with y != 0, so chi(1 + t^2) = chi(x(Q)). For j = 0 this is +1 (Proposition 5 (i)); for j = 1 it is chi(2) = -1 as p = 5 mod 8. []

Consequence. For p = 5 mod 8, S_{p,1} contains both parities as soon as both roots of a pair +-t are in it (for example p = 557, S_{p,1} = {42, 111, 169, 238}). S_{p,0} can mix parities only across different pairs of roots. A prime with two roots has a single-parity S_{p,0}.

## Proposition 8 (parity obstruction for pairs of primes). Proof given; hypotheses verified for 149 and 197
Let p != q be primes, p = q = 5 mod 8, and fix j. Suppose that every index of S_{p,j} has one parity and every index of S_{q,j} has the other. Then S_{p,j} and S_{q,j}, read as periodic subsets of the integers (period m_p, m_q), have empty intersection.

Proof. Both periods are even (Proposition 6 (a)), so the parity of an integer is determined by its residue modulo m_p and modulo m_q. An integer congruent to an element of S_{p,j} modulo m_p is of the parity of that set, and likewise for q; they differ. []

The prime pair (149, 197): m = 84 and 92, S_{149,0} = {16, 68} (both even), S_{197,0} = {33, 59} (both odd), gcd = 4; the hypotheses hold, and the pair is one of the 29 incompatible pairs below 2000 on the nP branch. It does not require GRH, Chebotarev, or any independence assumption. It explains pairs of this type and no others: the pair (149, 631) is incompatible but 631 = 7 mod 8, and the code finds 4 (pair, branch) cases below 2000 that satisfy the hypothesis, all incompatible.

## Observed
1. Counterexamples to |S_{p,0}| <= 4 (an earlier conjecture, withdrawn): p = 85453 (= 5 mod 8, 13 mod 24) has |S_{p,0}| = 8 (m_p = 42804); p = 32237 (= 5 mod 8, 5 mod 24) has |S_{p,1}| = 8 (m_p = 16168). Both are below the proved bound 12.
2. Largest |S| below 4000, by (p mod 4, #R_p) and branch: (1,2): 4, 4; (1,6): 2, 4; (3,2): 2, 2; (3,6): 4, 6 (branches 0, 1); all within Proposition 3.
3. Search for |S| = 12, all primes up to 3·10^7 (code/search_support_twelve.py, about 6 minutes, data/support_twelve_search_3e7.txt): the filters of Proposition 4 and the other necessary tests leave 53 primes, all = 1 mod 24 (none = 5 mod 24); of the 106 (prime, branch) cases, |S| = 0 (23), 2 (26), 4 (29), 6 (3), 8 (24), 12 (1: p = 5251537, branch 1). On branch 0 the largest value found is 8. Limits: only primes passing the filters are examined; the filters are proved necessary (Proposition 4; primes below 29 are skipped, which is safe because p = 5 is the only prime below 29 that is 1 or 5 mod 24 and m_5 <= 10 < 12), so no prime below 3·10^7 other than 5251537 has |S| = 12 on either branch, assuming the code is right.
4. The sums over primes 5 <= p <= 30000 (code/support_density_sum.py, data/support_sum_30000.txt): sum |S_{p,0}|/m_p = 0.414, sum |S_{p,1}|/m_p = 0.329; sum |N|/m_p = 0.940, 0.925; active primes 218, 219; largest |S| seen 4, 6. The sums grow slowly (the increments are of the size of a constant times d(log log p)) and are a heuristic measure only; no theorem is claimed, and they say nothing about infinitely many neutral indices.
5. Dossier counts below 2000 (reproduced exactly): 28 active primes on some branch; on the nP branch 17 active primes, 136 pairs, 62 with gcd(m_p, m_q) > 1, 29 incompatible; on the nP + T branch 19, 171, 66, 32.

## Open
1. Infinitely many incompatible pairs. Proposition 8 gives a mechanism, not a family. One needs infinitely many active primes = 5 mod 8 with qualifying roots of each parity; the parity is a quadratic character at a root (a finite Galois condition), but "active" also requires the point to lie in <P mod p>, which is not a splitting condition of H (a Kummer-type question for P).
2. Whether the root-level characters chi(r + i), together with the Galois action on the roots, force any parity distribution among the eligible primes p = 5 mod 8. This can be separated from the accessibility of the orbit and might admit a Chebotarev argument; not attempted here.
3. |S_{p,0}| = 12 on the nP branch: no example below 3·10^7; the necessary condition is p = 1 mod 24.
4. Parity for p = 1 mod 8 and for p = 3 mod 4 (no usable second descent).
5. A formalization of Propositions 1, 2, 3 and the algebra of Proposition 4 in Coq; scheduled. The elliptic-curve parts (Propositions 5 to 6) are outside what the Coq files check.

## Reproduce
python3 code/verify_support_structure.py            (about 8 s; --quick about 7 s)
python3 code/search_support_twelve.py 30000000      (about 6 minutes; stdlib; writes to stdout)
python3 code/support_density_sum.py 30000 data/support_sum_30000.txt   (about 35 s)
