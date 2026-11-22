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

## Second file (code/coq/F28_divisibility.v): fidelity audit
Status: derived with a language model; no human has checked it; compiled only in CI (the sandbox has no Coq).
The owner's file repeats the two identities of the first file and adds divisibility lemmas. Findings:
- The lemmas (divide_product, divide_difference) and the three implications are correct and match the three cases of the paper (section 3, Setup): if p | F and p | c then p | 4a^3; if p | F and p | b then p | 4a^3; if p | F and p | a then p | 27 b^2 c. They hold for every integer p; no primality or size is used.
- They do not by themselves state what the paper uses, that a prime p >= 5 dividing F does not divide abc. That needs (i) primality of p (Euclid's lemma) and p >= 5, to remove the factors 4 and 27; (ii) a^2 + b^2 = c^2 and gcd(a,b) = 1, which the paper uses to pass from "p | a and p | c" to "p | b" and to get the contradiction with coprimality ("p | a, then p | 27b^2c, p does not divide b because gcd(a,b) = 1, and p does not divide c because c^2 = a^2 + b^2"). The file's title "F.28 - arithmetic formalization" therefore overstates it; the closing comment "no additional Qed is required" is harmless.
- Added in review (Part V): F28_prime_not_dividing_abc: for prime p >= 5, a^2 + b^2 = c^2, Z.gcd a b = 1 and p | F a b c, p divides none of a, b, c; with helper lemmas (prime_div_sq, prime_div_cube, ge5_div_4a3, ge5_not_div_27, coprime_contradiction). Its contrapositive gives the paper's "if p | c then F = 4a^3 (mod p) is not 0".

Fidelity table (both files)
| paper claim | Coq theorem | match |
| Delta numerator -1024 F (rational model) | F28_discriminant_identity | exact; the integral-model version is F28_discriminant_integral_model |
| (-c6/p) = (ab/p) for p | F, algebraic core | F28_character_identity | the ring identity only; the symbol manipulation is not formalized |
| p | F, p | c => p | 4a^3 etc. (section 3) | F28_if_p_divides_{a,b,c} | exact for all integers p |
| p >= 5, p | F => p does not divide abc | F28_prime_not_dividing_abc | exact, with the hypotheses of the paper |
| a, b, c from a rational t; reduction types; local root numbers; Rizzo's tables; Appendix B | none | not formalized |

## Third file (code/coq/F28_reduction.v): fidelity audit
Status: derived with a language model; no human has checked it; compiled only in CI.
- F28_nondivisibility_reduction is correct as a conditional statement: from p | F and four assumptions (no common divisor of a and b; (p | 4a^3) implies (p | a); (p | 27b^2c) implies (p | b) or (p | c); (p | a) and (p | c) imply (p | b)) it derives that p divides none of a, b, c; the proof only combines the three implications of the second file with these assumptions. I read the case analysis line by line and it is valid.
- It is a reduction, not the nondivisibility itself: the four assumptions are where primality, p >= 5, a^2 + b^2 = c^2 and gcd(a,b) = 1 enter, and the file does not prove them. So it must not be cited as machine-checking "p does not divide abc". (The title "NONDIVISIBILITY REDUCTION" is honest; the name of the theorem could be misread.)
- Added in review: F28_reduction_hypotheses_hold proves the four assumptions for every prime p >= 5 with a^2 + b^2 = c^2 and Z.gcd a b = 1 (so the reduction is not vacuous), and F28_nondivisibility_prime combines both: the unconditional statement, the same as F28_prime_not_dividing_abc of the second file, now obtained through the owner's reduction. The helper lemmas are repeated from the second file because each file is a separate compilation unit; a shared project layout (a _CoqProject with imports) can replace the repetition if more files arrive.

| paper claim | Coq theorem | match |
| p >= 5, p | F => p does not divide abc, as a reduction to four listed facts | F28_nondivisibility_reduction | exact, conditional on the four facts |
| the four facts for primes p >= 5 and a primitive triple | F28_reduction_hypotheses_hold (added) | exact |
| the unconditional statement | F28_nondivisibility_prime (added), F28_prime_not_dividing_abc (second file) | exact, with the hypotheses of the paper |

## Fourth to sixth files (code/coq/F28_arithmetic.v): fidelity audit
Status: derived with a language model; no human has checked it; compiled only in CI.
- The owner sent three consecutive versions of one consolidated file; each regroups the earlier ones (identities, divisibility helpers, conditional reduction) into labelled parts and adds lemmas. I diffed them against each other: the sixth contains the fourth and fifth, so only the sixth is recorded.
- New lemmas, all correct: `F28_primitive_coprimality` (5 <= p, gcd a b = 1 gives not (p | a and p | b); holds for every integer p >= 5), `F28_pythagorean_square_divisibility` (a^2 + b^2 = c^2, p | a, p | c give p | b^2; any integer p), `F28_prime_square_cancel` (p prime, p | x^2 gives p | x; the proof by prime_mult with both factors equal is sound) and `F28_pythagorean_prime_divisibility` (p prime, p | a, p | c give p | b: the last assumption of the reduction).
- So the owner's file now discharges two of the reduction's four assumptions (coprimality and the Pythagorean one). The two cancellation assumptions (4a^3 and 27b^2c) are still not proved there: they need p prime and p >= 5 (p does not divide 27 = 3^3). Added in review: `F28_ge5_div_4a3`, `F28_ge5_not_div_27`, `F28_reduction_hypotheses_hold` (all four assumptions for a prime p >= 5 and a primitive triple) and `F28_nondivisibility_prime` (the unconditional statement). Same statement as F28_prime_not_dividing_abc (second file) and F28_nondivisibility_prime of F28_reduction.v; F28_arithmetic.v supersedes both as the single file to read, and they stay for history.

| paper claim | Coq theorem | match |
| the first assumption: p >= 5, primitive triple | F28_primitive_coprimality | exact (holds for every integer p >= 5) |
| p | a and p | c give p | b (p prime) | F28_pythagorean_prime_divisibility | exact |
| 4a^3 and 27b^2c cancellation for p >= 5 | F28_ge5_div_4a3, F28_ge5_not_div_27 (added) | exact |
| the unconditional statement for primes p >= 5 | F28_nondivisibility_prime (added) | exact |
