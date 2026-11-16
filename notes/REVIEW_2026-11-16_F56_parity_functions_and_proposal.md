# Review, 16 November 2026: F.56 (coprimality of ab with F, the parity functions h_n and h~_n) and a research proposal that uses them

Status: language-model derivation and assessment. No human has checked the proofs or this assessment.

## 1. What F.56 adds

Most of what a proposal "Transferring Prime-Factor Parity Results to Problem H" (dated 16 November 2026, status "proposed strategy for independent review") needs was already in the paper: the identity 4a^3 + 27b^2c = -4F(U,V)/d^3 ("The prescribed parity"), the exact root-number formula for every t (F.28), kappa_n and the decomposition W = eps_n delta_n kappa_n (F.24), and Corollary D2. F.56 adds only these:

* (a) a short proof that no prime p >= 5 dividing F divides ab, so every symbol (ab/p) is +-1 and (ab/M) is always defined; and (ac/p) = (-3/p), hence (ab/p) = (-3bc/p);
* (b) the two parity functions h_n = (-1)^{#Q_n} = (-1)^{omega(R)}(ab/R) (this is W(E_{t_n}) for n >= 2, since f(t_n) = +1 by F.53) and h~_n = (-1)^{Omega_Q} = lambda(N_n)(ab/N_n), with h_n h~_n = kappa_n = (-1)^{D_n}, D_n = #{p : chi_p = +1, e_p even};
* (c) the transfer inequality |H - H~| <= 2 D(X), and why it is no route to Problem H;
* (d) the reciprocity form of (ab/N_n), in which the factor (N/q) is elementary (local table at the primes dividing ab); this is the mechanism of the period-6 law of F.53;
* (e) the check script code/verify_jacobi_identities.py.

## 2. Assessment of the proposal

* Valid: h~ h = (-1)^D, the transfer inequality, and (C) => (B).
* Not available: hypothesis (A), cancellation of lambda(N_n)(a_n b_n / N_n) along the orbit. It is the Chowla-type input of F.24 and F.27; the only related unconditional work found (not read; title seen) concerns reducible cubic forms (Helfgott, arXiv math/0408142).
* Not available unconditionally: (B)/(C), a density bound for primes with even exponent. Fixed primes are understood (formal-group lift from r_p to p r_p, density about 12/(p r_p)); the tail over all p needs a uniform square-divisor estimate on an exponentially thin sequence. Even abc (as recalled, not verified: squarefull part of N_n at most about N_n^{1/3+eps}) leaves a middle range of primes.
* Observed (F.56 (c)): for n <= 2000 and 5 <= p < 8000, p^2 | F_n for 19 values of n (0.95%), 17 with p = 23 in the classes 32, 198 mod 230 = 23 * r_23, two with p = 83.
* The 2-adic law (F.55) is independent of odd-prime multiplicities.
* Conclusion: a clean decomposition, but all the difficulty is in (A); it does not reduce Problem H.
* Correction of an earlier remark in the same review: (N/q) in the reciprocity expansion is not the hard part; it is elementary (F.56 (d)). The hard part of h~_n is lambda(N_n).

## 3. Approximation question (added at revision 266)

The F.54 remark and F.55 (f) now say that the 2-adic law proves distinctness of the integers F(t_n) without any information on how close t_n comes to the real roots of D. It gives only |D(t_n)| >= V_n^{-6} (from F_n != 0). A non-trivial lower bound for |D(t_n)| is Open and is not used by F.55; the |F_n| are not shown to be distinct.
