# Primes with support exactly two: what is provable, and the missing step

Status: derived with a language model, 19 November 2026; no human has checked it. No consequence for Problem H; the paper is not changed. Code: code/verify_support_two.py (standard library only, about 6 seconds to 10^4) and code/support_two_densities.py (numpy, reads the model of G in code/verify_group_G.py). Answers the independent review request "infinitely many primes with support exactly two?" (owner attachment; the question text is not stored in the repo).

## Definitions (as in the request)
C: y^2 = x^3 - 2x^2 + 2x, P = (1,1), T = (0,0), t(Q) = 1 - x(Q), H(t) = t^6 - 30t^4 - 24t^2 - 1, a(t) = 2t(1 - t^2), d(t) = (1 - t)(1 + t^2). For a prime p >= 5, R_p = {Q in C(F_p): H(t(Q)) = 0, (a(t)/p) = +1} (a union of +-pairs) and S_p = R_p intersected with <P mod p> (n P with x(nP) = 1 - t). So |S_p| is even and S_p is contained in R_p.

## Result: no proof of infinitude
I do not have a proof that #{p: |S_p| = 2} is infinite, and I do not see one with current unconditional tools. Everything below is what can be proved, and the precise step that is missing.

## Audit (reproduced, code/verify_support_two.py)
1. disc H = 2^6 3^18 23^2, disc f = 3^9 23 (f(z) = z^3 - 30z^2 - 24z - 1), N(a(t)) = -2^8 3^6, N(d(t)) = -2^7 3^3 (exact resultants). So the radicands are units away from 2 and 3, L is ramified only at 2, 3, 23, and 7 is unramified. The Chebotarev reduction for |R_p| is correct.
2. p = 7: H has roots 3, 4; only t = 3 has a(t) and d(t) both squares; R_7 = {(5, +-1)}, |R_7| = 2. S_7 is empty because x = 5 is a non-residue mod 7 (so the pair is outside ker delta, below, hence outside <P>).
3. Scan, 5 <= p < 10^4 (1227 primes): |S_p| = 0 for 1153, = 2 for 63, = 4 for 11. |R_p| = 0, 2, 4, 6, 8 for 1003, 180, 35, 8, 1. The first primes with |S_p| = 2: 149, 197, 547, 631, 1187, 1223, 1229, 1319, 1483, 1511, 1619, 1747.
4. |S_p| = 2 does not force |R_p| = 2: of the 63 primes with |S_p| = 2, 57 have |R_p| = 2 and the other 6 have |R_p| > 2.
5. Exceptional primes: 2, 3, 23 (at 23, H has a double root and R_23 is empty).

## What is provable
1. Positive density of |R_p| = 2. From the explicit model of G (F.57 (b'), order 24576, code/support_two_densities.py; the model is a computation with floating-point signs): 3798/24576 = 633/4096 = 0.1545. Observed below 10^4: 180/1227 = 0.147.
2. The 2-isogeny and an even index. C' : Y^2 = X^3 + 4X^2 - 4X is 2-isogenous to C, with dual isogeny phi_hat: C' -> C, phi_hat(P') = P for P' = (2, -4) (exact check). The connecting map delta: C(F_p) -> F_p^*/F_p^*2, Q -> x(Q), T -> 2, has kernel phi_hat(C'(F_p)), of index exactly 2 in C(F_p) (|C'(F_p)| = |C(F_p)| and ker phi_hat has order 2); the code verifies |ker delta| = N_p/2 for every p. Since P = phi_hat(P') lies in ker delta, m_p divides N_p/2 and [C(F_p) : <P>] is even for every odd good p (minimum 2 below 10^4). So the Lang-Trotter / Gupta-Murty density of primes with P a generator of C(F_p) is 0 here, and the right Artin-type quantity is j_p = [ker delta : <P>] (equivalently <P', T'> = C'(F_p)). j_p = 1 for 592 of the 1227 primes.
3. A finite-level split. Suppose |R_p| = 2, with root t (up to t <-> -t).
   - Class B, (1 - t / p) = -1: then x = 1 - t is a non-residue, Q lies outside ker delta, so outside <P>, and S_p is empty. Density 1926/24576 = 321/4096 = 0.078. Checked: 96 of 96 primes below 10^4 (a positive-density counterexample to "|R_p| = 2 implies |S_p| = 2").
   - Class A, (1 - t / p) = +1: then Q lies in ker delta. Density 1872/24576 = 39/512 = 0.076. If moreover j_p = 1, then <P> = ker delta, so S_p = R_p and |S_p| = 2. Checked: 42 of 42 primes with j_p = 1 have |S_p| = 2. Without the condition j_p = 1: 57 of the 84 class-A primes below 10^4 have Q in <P>.
4. Upper bound: the primes with |R_p| = 2 and S_p nonempty have upper density at most 39/512.

So #{p: |S_p| = 2} would be infinite as soon as infinitely many primes lie in class A with j_p = 1 (or with Q in <P>). This is an Artin-type statement for the non-CM curve C' (c_4 = -32, Delta = -256, j = 128), inside a prescribed Frobenius class of L*.

## Routes
Route A (conditional on GRH). Adapt the Lang-Trotter / Gupta-Murty / Cojocaru-Murty sieve (the elliptic analogue of Hooley) to {p in class A: <P', T'> = C'(F_p)}. Lemmas: (i) the 2-adic and l-adic images for C', including the index forced by the rational 2-isogeny; (ii) the Kummer degrees of P' (the field Q(C'[m], P'/m)); (iii) the intersection of L* with Q(C'[m], P'/m): L* contains i and sqrt 2 (so zeta_8), and, I believe (not checked here), sqrt(-69) from disc f, so there is entanglement at levels 2^k, 3 and 23, and the density needs a correction factor for it. Output: a conditional theorem and an explicit constant to compare with the data.

Route B (unconditional but weaker). The shifted-gcd bound of F.57 (e) together with size arguments gives primitive prime divisors of F_n, hence |S_p| >= 2 for some p. It does not give |S_p| = 2, because nothing controls |R_p| (the Frobenius distribution of prime divisors of F_n is open), and the sign condition ((a_n b_n)/p) = +1 is essentially Problem H.

A non-Artin handle would be a Koblitz-type input: if |C(F_p)| = 2q with q prime, then <P> = ker delta and class A gives S_p = R_p. That input is open.

## Assessment
Infinitude of |S_p| = 2 most likely needs an elliptic Artin-type input, conditional on GRH. The 2-isogeny reduces "P primitive" to "index 2 in ker delta" but does not remove the input.

## What it rests on
Exact algebra (Fractions) for item 1 of the audit and for phi_hat(P') = P; a full scan below 10^4 for the counts; the explicit model of G (F.57 (b'), floating-point signs, |G| = 24576 from F.5) for the densities. Not a literature search: the Route A lemmas are stated as a plan, with the entanglement claim about sqrt(-69) unchecked.

## Second round (same day): audit of the follow-up brief "support-two progress"
Code: code/support_two_affine_probability.py (standard library, about 3 seconds, in CI); the extra norms are in code/verify_support_two.py. Derived with a language model; no human check.

Error found. The local probability beta_l that l divides j_p in the maximal affine model F_l^2 x| GL_2(F_l) (l odd) is beta_l = (l^3 - l - 1) / (l^2 (l-1)^2 (l+1)), not (l^2 - 2) / (l^2 (l^2 - 1)). Brute force over all (A, v): l = 3: 23/144 (the other formula gives 7/72), l = 5: 119/2400 (23/600), l = 7: 335/14112 (47/2352). Derivation: with g = (A, v), kappa_P = v mod (A - I)V and kappa_T = 0 for odd l; the condition fails when A = I (probability 1/(l (l-1)^2 (l+1))) and, when dim ker(A - I) = 1 (probability (l^2 - l - 1) / (l (l-1)^2)), with probability 1/l. Both versions are of size l^-2, so the sum converges and the brief's conclusions do not change.

Checked and correct: j_p = [E(F_p) : <P', T'>] = #C / (2 m_p) (no mismatch on 428 primes below 3000); delta_p never trivial; for p = 3 (mod 8), j_p is odd (all primes below 3000; all 29 favorable primes below 10^4); psi_3 = 3X^4 + 16X^3 - 24X^2 - 16; the Kummer criterion (coinvariants V / (F - I)V, kappa_T = 0 for odd l); K_l unramified outside 2 and l (including l = 2); the p = 1187 witness (#C = 1222 = 2 * 13 * 47, ord P = 611, j = 1, roots 411 and 776, only t = 776 qualifies with x = 412 a square); the class-A index distribution (42, 13, 8, 4, 3, 2, 1, 1, 2, 1, 1, 1, 3, 1, 1; 15 primes with Q_p in <P> and j_p > 1). Q(zeta_8) is already contained in L* (i and sqrt 2), so L* Q(zeta_8) = L*. The count of good primes 5 <= p < 10^4 is 1227 (pi(10^4) - 2); the brief's 1226 omits one prime (probably 5 or 23).

Ramification of L* (exact). The radicands 1 - t, 1 + t, 1 + t^2, a(t), d(t) have norms -54, -54, 2^6, -2^8 3^6, -2^7 3^3 over Q[t]/H, so every radicand is a {2, 3}-unit in the splitting field N of H; the Kummer layer is unramified outside 2 and 3, and disc H = 2^6 3^18 23^2 gives ramification of N at 2, 3, 23 only. Hence L* is ramified only at 2, 3, 23.

Densities. A scan of all 13846 primes 5 <= p <= 1.5 * 10^5 gives |R_p| = 2 for 0.1601 (model 633/4096 = 0.1545, z = 1.8), class A 0.0797 (39/512 = 0.0762, z = 1.6), class B 0.0804 (321/4096 = 0.0784, z = 0.9): consistent with the model, not a certificate.

Finite-set proposition (correct). For any finite set of primes avoiding some favorable prime with j_p = 1 (1187 or, e.g., 149, 197), the favorable primes with gcd(j_p, product) = 1 have positive density (conjugacy-invariant condition in K_l, unramified at the witness, Chebotarev). It does not give j_p = 1 itself, which needs all levels at once.

Literature. arXiv:2304.03964 (read from its abstract page only): Theorem 1.2 characterises locally l-imprimitive points; our P = phi_hat(P') is its case (C) with l = 2. As read there, the density for "P generates E(F_p)" is only an upper density in general, and is not shown to be the true density even under GRH when positive. Moree-Stevenhagen, "A two-variable Artin conjecture" (2000), is the multiplicative analogue of "Q_p in <P>" and is proved under GRH; I know of no elliptic analogue. Gupta-Murty and Cojocaru-Murty are recalled from memory and unchecked.

Open and unchecked: positivity of d_infinity (needs Serre's open image theorem and Bashmakov-Ribet for the Kummer images at large l; not written out); the uniform estimate (A); independence of P and Q modulo torsion over F_0 = Q(t, sqrt d).

Strongest rigorous statement now (Chebotarev only, with the facts about L* above): class A has positive density; for every finite set avoiding a favorable j = 1 prime, favorable primes with gcd(j_p, product) = 1 have positive density (e.g. gcd(j_p, 6) = 1); S_p is empty on class B and on {R_p empty}; the upper density of {|R_p| = 2, S_p nonempty} is at most 39/512. Infinitude of |S_p| = 2 remains open.
