# Coq file for F.28: what it checks and what it does not

Status: derived with a language model, 22 November 2026; no human has checked it. No consequence for Problem H; the paper is not changed. File: code/coq/F28_identities.v (owner's four theorems unchanged, plus a part added in review); CI: .github/workflows/coq.yml (installs Coq with apt, compiles with coqc, requires that Print Assumptions reports no axioms). The reviewer's sandbox has no Coq, so the file was not compiled locally; every identity (the owner's and the added ones) was checked on 20000 random integer tuples in Python, and the compilation result is the CI run on this PR.

## The owner's file
- Theorem 1 (character identity): a^3 (-6912 b) = 216^2 b^3 c - 1728 b F(a,b,c) with F = 4a^3 + 27 b^2 c. A true ring identity (both sides equal -6912 a^3 b). It is the algebraic core of the step (-c6/p) = (ab/p) for a prime p | F: modulo F it says -6912 a^3 b = (216 b)^2 b c, and -6912 = -3 * 96^2, so -3a = c up to squares, i.e. (c/p) = (-3a/p); then (-c6/p) = (-6912 b c^5/p) = (-3bc/p) = (-3b/p)(-3a/p) = (ab/p). The Legendre-symbol steps are not formalized.
- Theorem 2 (discriminant): -16 (4 (4a)^3 + 27 (-8b)^2 c) = -1024 F. True. It is the numerator after clearing c^3 for the model y^2 = x^3 + 4(a/c)x - 8(b/c) (Delta = -1024 F / c^3, as in the comment); it is not the discriminant of the model with A = 4a, B = -8b. The paper's integral model Y^2 = X^3 + 4ac^3 X - 8bc^5 has Delta = -1024 c^9 F, added below.
- Theorems 3 and 4 (c4, c6): proved by reflexivity from the definitions c4_num a := -192 a and c6_num b := 6912 b. They are definitional, not identities with content; c4_num and c6_num also omit the powers of c (c4 = -192 a c^3, c6 = 6912 b c^5 for the integral model).

## Added in review (all by ring)
- the integral model: -16 (4 (4ac^3)^3 + 27 (-8bc^5)^2) = -1024 c^9 F; c4 = -48 * 4ac^3 = -192 a c^3; c6 = -864 * (-8bc^5) = 6912 b c^5;
- the triple and the sextic form: F(V^2 - U^2, 2UV, U^2 + V^2) = -4 (U^6 - 30 U^4 V^2 - 24 U^2 V^4 - V^6). The paper writes F both ways; they differ by the factor -4, so the primes p >= 5 are the same;
- Delta = 2^12 c0^9 F(U,V) for a = V^2 - U^2, b = 2UV, c0 = U^2 + V^2 (the identity stated in F.28);
- the coprimality step of the proof: F(U,V) = -54 V^6 + (U^2 - V^2)(U^4 - 29 U^2 V^2 - 53 V^4) and F(U,V) = -8 V^6 + (U^2 + V^2)(U^4 - 31 U^2 V^2 + 7 V^4), so a prime p >= 5 dividing F divides neither V^2 - U^2 nor c0 unless it divides 54 V^6 or 8 V^6 (and then p | V, which forces p | U).

## What is not formalized
The reduction type (multiplicative at p | F because p does not divide c4), the local root numbers (-1 split, +1 non-split), the local signs at 2, 3 and at primes dividing c (Rizzo's tables), Appendix B, the product formula and its Jacobi-symbol form, and the quadratic-character reasoning. So F.28 as a whole is not machine-checked; what is checked is the list of polynomial identities above. A status line for the paper could read "the polynomial identities used in the proof are machine-checked in Coq (ring); the rest is not"; the paper is not edited here (the claude.ai document is the source of truth).
