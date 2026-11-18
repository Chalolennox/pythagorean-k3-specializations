<!-- Provenance: independent validation of the shifted-gcd proposition, sent to the chat by the repository owner on 18 November 2026 (attachment text). The text below the line is unmodified. Assessment in notes/REVIEW_2026-11-17_gap_k_classification.md, section 6. -->
---
Validation of the shifted-gcd theorem
I think the reviewer's main claim can be proved, with an important qualification: the valuation bound is valid for primes p>=5 at which kP does not reduce to the identity, provided N_k is the full, correctly normalized resultant.

The key is to use the Bezout identity for resultants. This avoids the uncertain step in the reviewer's Cayley-Hamilton argument.

Recall C: y^2=x^3-2x^2+2x, P=(1,1), h(X)=H(1-X), H(t)=t^6-30t^4-24t^2-1.

For a fixed gap k, let G_k(X,Z)=Phi(X,Z,x(kP)) be the addition-law correspondence, and define N_k=Res_X(h(X), Res_Z(h(Z),G_k(X,Z))).

The proposed theorem. Suppose N_k != 0, and let m_p denote the order of P in C(F_p). Then, for p>=5 satisfying m_p not dividing k, v_p(gcd(F_n,F_{n+k})) <= v_p(N_k) for every n>=1, where F_n is the primitive discriminant factor used in Problem H. Here v_p of a rational resultant is understood through its numerator and denominator. The restriction m_p not dividing k is essential: it ensures that kP has finite reduction and the coefficients of G_k are p-integral.

Proof.
Step 1. Relate F_n to h(x(nP)). Write t_n=u_n/v_n in lowest terms, and let d_n be the primitive normalization factor. The polynomial identity 4(v^2-u^2)^3+27(2uv)^2(v^2+u^2) = -4v^6 H(u/v) gives F_n = -4 v_n^6 H(t_n)/d_n^3. Since d_n is a power of 2, it is a unit at every p>=5. If p | F_n, then p does not divide v_n: if p | v_n, the displayed polynomial reduces to -4u_n^6, which is nonzero modulo p. Consequently, whenever p^e | F_n, h(x(nP)) = 0 mod p^e. The same holds for n+k.
Step 2. Integrality of the gap correspondence. The curve C has good reduction at every p>=5. If m_p does not divide k, then kP does not reduce to the identity. Therefore its affine coordinates, including x(kP), are p-integral. The coefficients of the explicit polynomial G_k are consequently in R=Z_(p). Moreover, the elliptic addition law gives the exact identity G_k(x(nP),x((n+k)P))=0. This is a polynomial identity, so it remains valid even at points where a rational addition formula would have a denominator.
Step 3. Resultant identities. Set R_k(X)=Res_Z(h(Z),G_k(X,Z)). Because the polynomials have coefficients in R[X], the resultant Bezout identity gives polynomials A,B in R[X,Z] such that R_k(X)=A(X,Z)h(Z)+B(X,Z)G_k(X,Z). Now suppose p^e | gcd(F_n,F_{n+k}). Substituting X=x(nP), Z=x((n+k)P), we obtain R_k(x(nP)) = 0 mod p^e. Apply the resultant identity a second time: N_k=U(X)h(X)+V(X)R_k(X), for suitable U,V in R[X]. Substituting X=x(nP) gives N_k = 0 mod p^e. Hence e <= v_p(N_k). Taking e=v_p(gcd(F_n,F_{n+k})) proves the asserted bound.

What remains to verify. The algebraic argument is complete under its stated definitions. Before calling this a certified theorem for the reviewer's numerical N_k, three details need checking:
1. Normalization: the computed N_k must be the full nested resultant of the stated h and G_k, not a square-root factor, reduced resultant, or differently scaled integer.
2. Nonvanishing: N_k != 0 must be established for each gap under consideration. Otherwise the bound is vacuous.
3. Branch conventions: the same proof works for nP+T, but its F_n must use the corresponding primitive coordinates.
The reported p=23 example is consistent with the theorem but is no longer needed to justify the general argument.

Stronger consequence. For fixed k with N_k != 0, every prime p>=5 satisfying m_p not dividing k and dividing both F_n and F_{n+k} must divide the numerator of N_k. Thus the possible common primes are confined to a finite, explicitly computable set. In fact, the valuation bound also gives a uniform bound on the part of the gcd supported at these primes: the product over p>=5, m_p not dividing k, of p^{v_p(gcd(F_n,F_{n+k}))} divides the product of p^{v_p(N_k)}. The right-hand side depends on k, not n.

My assessment has changed: the reviewer's valuation argument is essentially correct. The missing justification was the integral resultant evaluation, and the two Bezout identities supply it.

This is worth recording as a proposition in the paper, with the precise normalization and nonvanishing conditions. It is a rigorous shifted-gcd statement, although it does not establish the sign correlations needed for Problem H.
