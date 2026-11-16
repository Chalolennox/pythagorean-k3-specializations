<!-- Provenance: working note PROOF_C_consolidated.md; the proof of F.55 in Appendix F is written from it with the paper's notation (psi, U, V, F_n, Gamma, Lambda replace W, A, B, N, G, E)
     Reviewed source text, word for word, as of 16 November 2026 (delivery 2026-11-16d). Derived with a language model (Claude); not read by any human. -->

# The 2-adic law  v2(N_n - N_m) = 1 + v2(n^2 - m^2)  — one continuous proof (16 Nov 2026)

**Status: my derivation; no human has checked it.** It replaces the scattered notes by a single chain in which every interface (indices, normalizations, constants) is explicit. Where an older note differs, this document is the corrected one (in particular the block lemma is the improved one, and the reduction of (C) to (O2)/(E2) is written out). Each inequality used at an interface is tested in `verify_consolidated_interfaces.py`; that is a consistency check, not part of the proof.

**Theorem.** For integers n != m >= 1:  v2(N_n - N_m) = 1 + v2(n^2 - m^2), where N_n = Phi(A_n, B_n). Consequently n -> N_n, and n -> F(t_n) = -4N_n, is injective on positive integers.

**External inputs (all classical).** (F1) x(nP) = 1 - t_n; (F2) W_{2n} = 2 y(nP) W_n^4; (F3) the EDS recurrence W_{2m+1} = W_{m+2}W_m^3 - W_{m-1}W_{m+1}^3 and Ward's identity A_nB_m - A_mB_n = W_{n+m}W_{n-m}; (F4) the curve equation and chord formula. Plus: P has infinite order (Lutz–Nagell, `NOTE_coprimality_direct_proof.md` §0a). Nothing else is cited.

Notation. v = v2. C: y^2 = x^3-2x^2+2x, P=(1,1). W_n = psi_n(P): W_0..W_4 = 0,1,2,3,-20, W_{-n} = -W_n. A_n = W_{n-1}W_{n+1} (A_{-n}=A_n), B_n = W_n^2, t_n = A_n/B_n, u_n = B_n/A_n. alpha_n = A_n^2, beta_n = B_n^2. Phi(U,V) = U^6-30U^4V^2-24U^2V^4-V^6 = alpha^3 - 30 alpha^2 beta - 24 alpha beta^2 - beta^3. d := v(n^2-m^2). log, exp are the 2-adic ones; log is a homomorphism on 1+2Z_2 and an isomorphism 1+4Z_2 -> 4Z_2 (inverse exp), v(log(1+z)) = v(z) for v(z) >= 2.

## Part I. Arithmetic of W_n  (proved in `NOTE_coprimality_direct_proof.md`)
(I.1) W_n = n mod 2.  (I.2) v(W_n) = v(n) for n >= 1 (hence for all n != 0).  (I.3) gcd(W_n,W_{n+1}) = 1, so gcd(A_n,B_n)=1 and t_n = A_n/B_n is in lowest terms: (U_n,V_n) = (A_n,B_n), and N_n = Phi(A_n,B_n) is the paper's N_n.
Consequences used below: for odd n, B_n is odd, B_n = 1 mod 8, A_n is even with v(A_n) = v(n-1)+v(n+1) >= 3. For even n, A_n is odd, v(B_n) = 2v(n) >= 2. Ward + (I.2): for n != +-m,
  (W1) v(A_nB_m - A_mB_n) = v(n+m) + v(n-m) = d;  
  (W2) t_n - t_m = W_{n+m}W_{n-m}/(B_nB_m) has v = d for n,m odd;  u_n - u_m = -W_{n+m}W_{n-m}/(A_nA_m) has v = d for n,m even (also m=0, u_0 = 0).

## Part II. Two lemmas
**Block lemma (L).** Let g: Z -> Z_2 with v(g(a)-g(b)) >= v(a-b). Then for N >= 1 and every shift x, v( sum_{a<N} (N-a) g(x+a) ) >= v(N) - 1.
Proof. (i) For e >= 0: v(sum_{b<2^e} g(x+b)) >= e-1 and (ii) v(sum_{b<2^e} b g(x+b)) >= e-1. For e=0,1 direct (all terms integral; for (ii) e=1 the sum is g(x+1)). Step e -> e+1, e >= 1: put r_b = g(x+b+2^e)-g(x+b), v(r_b) >= e. Then sum_{b<2^{e+1}} g(x+b) = 2 sum_{b<2^e} g(x+b) + sum r_b, so v >= min(1+(e-1), e) = e. And sum_{b<2^{e+1}} b g(x+b) = 2 sum_{b<2^e} b g(x+b) + sum_{b<2^e} b r_b + 2^e sum_{b<2^e} g(x+2^e+b), with valuations >= e, >= e, >= e+(e-1) >= e. For N = 2^e u write a = j 2^e + b (j<u, b<2^e): N - a = 2^e(u-j) - b, so the sum is sum_j 2^e(u-j) [sum_b g(...)] - sum_j [sum_b b g(...)], valuations >= e+(e-1) and >= e-1. QED

**Second-difference lemma (S).** Let F: Z -> Q_2, xi: Z -> Q_2 with F(k+1)-2F(k)+F(k-1) = 2 xi(k). Put D_j = F(j)-F(j-1). For j < k, N = k-j:
  F(k) - F(j) = N D_j + 2 sum_{a<N} (N-a) xi(j+a).    (exact, telescoping)
Suppose v(xi(k)-xi(j)) >= lam + v(k-j) for all k != j, v(xi(j)) >= nu1 and v(D_j) >= nu0 for all j. Then v(F(k)-F(j)) >= v(k-j) + min(nu0, nu1, lam).
Proof. Write xi(j+a) = xi(j) + 2^lam g(a) with g Lipschitz-0 integral (g(0)=0). Then 2 sum (N-a) xi(j) = xi(j) N(N+1) has v >= nu1+v(N); 2^{lam+1} sum (N-a) g(a) has v >= lam+1+v(N)-1 = lam+v(N) by (L); N D_j has v >= v(N)+nu0. QED
(The constants nu0, nu1, lam are stated at each use: Part III: 6, 5, 4. IV.5: 3r+3, 3r+2, 3r+4. IV.6: 6, 5, 5.)

## Part III. Odd indices: (O2)  v(B_n-B_m) = d for odd n != m
For odd n = 2k+1 (k in Z; n -> -n is k -> -1-k) put T_k = (n^2-1)/8 = k(k+1)/2, E_k = log B_n - T_k log 9 (B_n in 1+8Z_2). Then E_0 = E_{-1} = 0 and E_{-1-k} = E_k.
**III.1 Recurrence.** Ward with (n,2), W_2^2 = 4, A_2 = 3: W_{n+2}W_{n-2} = 4A_n - 3B_n. Squaring, B_{n+2}B_{n-2} = B_n^2 (3-4t_n)^2. Take logs; T has second difference 1 so its part contributes log 9 = 2 log 3:
  E_{k+1} - 2E_k + E_{k-1} = 2 eps_k,  eps_k = log(1 - 4t_n/3),  eps_{-1-k} = eps_k.
t_n in 8Z_2 so v(eps_k) >= 5. By (W2), v(eps_k - eps_j) = 2 + v(t_n - t_{n'}) = 2 + v(n^2-n'^2) = 4 + v(k-j) + v(k+j+1) >= 4 + v(k-j) (when n != +-n'; if n = -n', eps equal).
**III.2 Lipschitz-4.** Apply (S) with F = E, xi = eps, nu0 = 6, nu1 = 5, lam = 4. (D_j = 2 sum_{i<j} eps_i for j > 0, D_0 = E_0-E_{-1} = 0, and D_j = -2 sum_{j<=i<0} eps_i for j < 0, so v(D_j) >= 6.) Hence for ALL integers j != k:
  v(E_k - E_j) >= 4 + v(k-j).
**III.3 Symmetry.** Take j = -1-k' (E_{k'} = E_{-1-k'}): v(E_k - E_{k'}) >= 4 + v(k+k'+1). N = k-k' and N' = k+k'+1 have opposite parity, so one of v(N), v(N') is 0 and
  v(E_k - E_{k'}) >= 4 + v(N) + v(N').
**III.4 Conclusion.** s = T_k - T_{k'} = N N'/2, v(s) = v(N)+v(N')-1, and n^2-n'^2 = 8s so d = 3 + v(s). w := log(B_n/B_{n'}) = s log 9 + (E_k - E_{k'}), v(log 9) = 3, so v(s log 9) = 3 + v(s) = d < 5+v(s) <= v(E_k-E_{k'}). Hence v(w) = d >= 3, B_n/B_{n'} = exp(w), v(B_n/B_{n'} - 1) = d, and since B_{n'} is odd, v(B_n - B_{n'}) = d. QED (O2)

## Part IV. Even indices: (E2)  v(A_n^2 - A_m^2) = 1 + d for even n != m
For even n put G_n = log alpha_n - (n^2/4) log 9 (alpha_n = A_n^2 in 1+8Z_2). G_0 = 0, G_{-n} = G_n.
**IV.0 Equivalence.** alpha_n/alpha_m = exp(w), w = ((n^2-m^2)/4) log 9 + G_n - G_m, v(first term) = d-2+3 = d+1. So (E2) <=> v(G_n - G_m) >= d+2 (then v(w) = d+1 >= 3 and v(alpha_n-alpha_m) = d+1).
**IV.1 Lattice recurrence.** Let h = 2^j, j >= 1. Ward twice (pairs (n,h-1),(n,h+1)): A_{n+h}A_{n-h} = W_{n+(h-1)}W_{n-(h-1)} W_{n+(h+1)}W_{n-(h+1)} = (A_nB_{h-1}-A_{h-1}B_n)(A_nB_{h+1}-A_{h+1}B_n) = A_n^2 B_{h-1}B_{h+1} (1-t_{h-1}u_n)(1-t_{h+1}u_n), and B_{h-1}B_{h+1} = A_h^2. Taking 2 log of the square and subtracting the quadratic part (second difference of n^2/4 with step h is h^2/2):
  G_{n+h} - 2G_n + G_{n-h} = 2G_h + 2e_h(n),  e_h(n) = log[(1-t_{h+1}u_n)(1-t_{h-1}u_n)].
Here t_{h+-1} = A_{h+-1}/B_{h+-1} with B odd, v(t_{h+1}) = v(h)+v(h+2), v(t_{h-1}) = v(h-2)+v(h); for h = 2^{r+1}, r >= 1: both equal r+2 (h=2: t_1 = 0, v(t_3) = 3). v(u_n) = 2v(n), and u is an isometry (W2). Therefore
  v(e_h(n)) >= (r+2) + 2v(n),  v(e_h(n)-e_h(m)) >= (r+2) + v(n^2-m^2),  e_h(0) = 0.
For h = 2: e_2(n) = log(1 + 40u_n/9) (t_3 = -40/9); this is the adjacent-sum identity (1-4t_{n+1}/3)(1-4t_{n-1}/3) = 1 + 40u_n/9, i.e. IV.1 with h=2 says G_{n+2}-2G_n+G_{n-2} = 2 eta_{n/2}, eta_k = e_2(2k), v(eta_k) = 5+2v(k), v(eta_k-eta_l) = 5 + v(k^2-l^2).
**IV.2 Step 1 (powers of two).** v(G_{2^s}) >= 2s+2 for s >= 2 (and G_2 = log 9 - log 9 = 0). From IV.1 with n = h, G_0 = 0, G_{-h} = G_h: G_{2h} = 4G_h + 2e_h(h). s=2: G_4 = 2e_2(2), v = 1+5 = 6. For h = 2^{s-1}, s >= 3 by induction: v(4G_h) >= 2+2(s-1)+2 = 2s+2 and v(2e_h(h)) >= 1 + s + 2(s-1) = 3s-1 >= 2s+2.
**IV.3 Step 2 (pairs (n,0)).** n = 2^r i, i odd, r >= 1; g = 2^r. On the lattice gZ solving the recurrence from G_0 = 0 with G_g given:
  G_n = i^2 G_g + 2 sum_{m=1}^{i-1} (i-m) e_g(gm).
v(i^2 G_g) >= 2r+2 (IV.2; G_2 = 0), and v(e_g(gm)) >= (r+1) + 2r (for r >= 2 v(t) = r+1; for r = 1, v(t_3) = 3), so the sum has v >= 1+3r+1 = 3r+2 >= 2r+2. Hence v(G_n) >= 2v(n)+2.
**IV.4 Step 3 (v(n) < v(m)).** d = 2v(n); v(G_n - G_m) >= min(2v(n)+2, 2v(m)+2) = d+2. (Includes m = 0.)
**IV.5 Step 4 (v(n) = v(m) = r >= 2).** n = 2^r a, m = 2^r b, a,b odd; h = 2^{r+1}; the coset 2^r(2j+1), j in Z, is stable under n -> n+-h and symmetric under j -> -1-j. Put Gt_n = G_n - (G_h/h^2) n^2. Then Delta_h^2 Gt = 2 e_h, Gt symmetric. Let F_j = Gt_{2^r(2j+1)}, xi_j = e_h(2^r(2j+1)): F_{-1-j} = F_j, xi_{-1-j} = xi_j, v(xi_j) >= (r+2)+2r = 3r+2 = nu, and by IV.1 v(xi_j - xi_{j'}) >= (r+2) + 2r + v((2j+1)^2-(2j'+1)^2) = 3r+4 + v(j-j')+v(j+j'+1) >= 3r+4+v(j-j'). D_0 = F_0 - F_{-1} = 0, D_j = 2 sum_{i<j} xi_i, v >= 1+nu. By (S) (nu0 = 3r+3, nu1 = 3r+2, lam = 3r+4): v(F_j - F_{j'}) >= 3r+2 + v(j-j'), and with j' -> -1-j' and opposite parity of j-j', j+j'+1:
  v(Gt_n - Gt_m) >= 3r+2 + v(j-j') + v(j+j'+1).
Now d = v(n^2-m^2) = 2r+2+v(j-j')+v(j+j'+1), so this is d + r >= d+2 exactly when r >= 2. The quadratic part (G_h/h^2)(n^2-m^2): v(G_h) >= 2(r+1)+2 (IV.2, r+1 >= 3), so it has v >= (2r+4) - 2(r+1) + d = d+2. Hence v(G_n - G_m) >= d+2.
**IV.6 Step 5 (v(n) = v(m) = 1).** k = n/2, l = m/2 odd. Put H_k = G_{2k}. IV.1 with h = 2 reads H_{k+1}-2H_k+H_{k-1} = 2 eta_k (H_0 = H_1 = 0, H_{-k} = H_k, eta symmetric, v(eta_k) >= 5, v(eta_k - eta_l) >= 5 + v(k-l)). Apply (S) with F = H, xi = eta, nu0 = 6, nu1 = 5, lam = 5 (D_j = H_j - H_{j-1} = 2 sum_{0<=i<j} eta_i for j > 0, D_0 = H_0 - H_{-1} = -H_1 = 0, so v(D_j) >= 6): hence v(H_k - H_l) >= 5 + v(k-l) for all k != l, and with l -> -l: >= 5 + v(k+l). So v(H_k - H_l) >= 5 + max(v(k-l), v(k+l)). For k,l odd, (k-l)+(k+l) = 2k has v = 1, so min(v(k-l),v(k+l)) = 1 and d = 2 + v(k-l) + v(k+l) gives 5 + max = d + 2. Hence v(G_n - G_m) >= d+2.
**IV.7 Conclusion.** n != m even, positive. If v(n) != v(m): IV.4. If equal: r = 1: IV.6; r >= 2: IV.5. So (E2) holds by IV.0. (Independent second route for the same statement: the reviewer's duplication proof, audited in `NOTE_odd_case_proof.md` Addendum 4; it needs IV.6's bound as its H3 and shares only Part I and Ward.)

## Part V. From (O2), (E2) to (C)
Let n > m >= 1, d = v(n^2-m^2). Write N = alpha^3 - 30 alpha^2 beta - 24 alpha beta^2 - beta^3.
**Odd–odd.** beta_n - beta_m = (B_n-B_m)(B_n+B_m), B_n+B_m = 2 mod 8, so v = d+1 (O2); beta^3-difference = (beta_n-beta_m)(beta_n^2+beta_n beta_m+beta_m^2), second factor odd: v = d+1. Others: from (W1) and B_n = B_m mod 2^d (O2): A_nB_m - A_mB_n = B_m(A_n-A_m) + A_m(B_m-B_n), so B_m(A_n-A_m) = (Ward term, v = d) - A_m(B_m-B_n), and v(A_m(B_m-B_n)) >= 3+d: hence v(A_n-A_m) = d; A_n + A_m = (A_n-A_m)+2A_m has v >= 3; so v(alpha_n - alpha_m) >= d+3. Then 24(alpha beta^2 diff): v >= 3+min(d+3, 6+d+1) = d+6; 30(alpha^2 beta diff): >= 1+(d+3+6) ; alpha^3-diff >= d+3+12. All >= d+2. So v(N_n-N_m) = d+1.
**Even–even.** v(alpha_n - alpha_m) = d+1 (E2); alpha_n^3-alpha_m^3 = (alpha_n-alpha_m)(odd), so main term has v = d+1. (alpha_n-alpha_m) = (A_n-A_m)(A_n+A_m) with (A_n-A_m)+(A_n+A_m) = 2A_n of v 1, so for an eps = +-1: v(A_n - eps A_m) = d. By (W1), A_nB_m - A_mB_n = (A_n - eps A_m)B_m + A_m(eps B_m - B_n), so A_m(eps B_m - B_n) has v >= d and v(B_n - eps B_m) >= d, and beta_n - beta_m = (B_n - eps B_m)(B_n + eps B_m), v(B_n+eps B_m) >= 1 (both even), so v(beta_n-beta_m) >= d+1. Then 30(alpha^2 beta diff) has v >= 1+min(d+2+4r, d+1) = d+2 (r = v(n) >= 1); 24 (alpha beta^2 diff): >= 3+(d+1); beta^3-diff >= d+1+8. If v(n) != v(m), say v(n) = r < v(m): d = 2r, v(beta_n) = 4r, v(beta_m) > 4r, and every non-main term has v >= 1+4r = d+... >= d+2 since 4r+1 >= 2r+2. So v(N_n-N_m) = d+1.
**Mixed parity.** n odd, m even (or reverse), d = 0. N_odd = -beta^3 - (terms of v >= 9) = -1 mod 8 (beta = 1 mod 16); N_even = alpha^3 + (terms of v >= 5) = 1 mod 8. So N_n - N_m = -2 mod 8: v = 1 = 1 + d. QED (C)

## Part VI. Interface table (what must match what)
| Interface | Statement | Where proved / tested |
|---|---|---|
| I -> III | B_n = 1 mod 8, v(t_n) >= 3, (W2) | Part I; script O |
| III.1 | E_0 = E_{-1} = 0, E symmetric, second difference 2 eps_k | exact identities; script O |
| III.2 | Lipschitz-4 for all integer pairs incl. negative | (S)+(L); script O (min slack 0) |
| III.4 -> V | (O2) with equality v(B_n-B_m) = d | exp/log on 1+4Z_2 |
| IV.1 | lattice recurrence for h = 2,4,8,16 exact | script E: 0 failures |
| IV.2 | v(G_{2^s}) = 2s+2 | script E |
| IV.4–IV.6 | v(G_n-G_m) >= d+2 for all even pairs | script E: 0 violations; IV.5 slack >= 3, IV.6 slack 0 |
| IV.0 -> V | (E2) <=> v(G_n-G_m) >= d+2 | exp/log |
| V | all three parity cases | script R: 6000 pairs, 0 failures |
Known loose points to look at first when auditing: (a) in Part V, the derivation of v(A_n - eps A_m) >= d from (W1) and (O2)/(E2); (b) in III.2 the constants: the three terms have valuations >= 6+v(N), >= 5+v(N), >= 4+v(N), so the Lipschitz constant is 4, not 5; (c) IV.5 uses v(G_h) from IV.2 with s = r+1 >= 3.

## What remains unproved
Nothing inside this document is left as a conjecture, but: no human has checked it; the external inputs are (F1)–(F4), Ward and the infinite order of P; the paper's own statement of F.54 is not changed. The older Lemma A (coefficient bounds) and the global collision question (u = +-t for F°) are not addressed here.
