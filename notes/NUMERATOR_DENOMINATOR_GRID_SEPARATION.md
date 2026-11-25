# Numerator–denominator grid separation

Let J: y²=x³−2x²+2x, P=(1,1), T=(0,0), x(jP)=m_j²/D_j² in lowest terms, l_j²=m_j⁴−2m_j²D_j²+2D_j⁴ with positive roots. Let h(x)=H(1−x), N_j=D_j¹²h(x(jP)). Paper F.20 gives gcd(N_j,6)=1 and m_j odd.

At every odd prime J has good reduction. If p divides m_j with valuation e, translation by T has x=2D_j²/m_j² and formal group depth e. Multiplication by k adds v_p(k) to depth, so for odd k v_p(m_kj)=e+v_p(k), and for even k v_p(D_kj)=e+v_p(k). The analogous denominator law holds for all k. If p divides l_j, reduction is another nonzero 2-torsion point; odd multiplication preserves it, even multiplication sends it to O. Since x is a local coordinate squared in the transverse direction at 2-torsion only after accounting for the ramification, the relevant depth here is v_p(y)=v_p(l_j); odd multiplication adds v_p(k).

Duplication gives m_2j=|m_j⁴−2D_j⁴| and D_2j=2m_jD_jl_j; no cancellation since m_j odd and odd common primes are excluded by the primitive equation. If p divides m_2j, jP reduces to exact order four with double T, hence 3jP reduces to −jP and 6jP to T.

Theorem: gcd(m_2j D_2j,N_j N_2j N_3j N_6j)=1 for all j≥1.
Proof: for p≥5 dividing m_j D_j l_j, all four reductions have order dividing two. At O the homogeneous sextic is a unit; at x=0 h=-54; modulo x²−2x+2 h=-8. For p dividing m_2j, the odd vertices satisfy x²=2, the even vertices reduce to T. The remainder of h modulo x²−2 is 338x−484 (corrects earlier erroneous 48x−66), and absolute resultant is 5768=2³·7·103. At p=7,103 the orders of P are respectively 6,54, so no order-four reduction is accessible. The primes 2,3 are excluded by F.20. QED, conditional only on the cited established inputs and finite-field calculations.

Owner-provided complete Magma V2.30-1 log 2026-11-25 18:35, seed 1778788015, 0.21s execution (1.3s displayed): all three resultants 54,64,5768 PASS; common-root polynomials u+3 and u+65; orders 6,54; zero accessible roots. All 30 seeds j=1..30 completed, 120 vertex visits, 60 doubling and 60 triplication edge checks, all four gcds equal 1 at every seed. Largest discriminant 121251 bits (180P). No factorization performed. This is an owner-run log, not an independently rerun Magma session. Human proof review pending.

Scope: propagation primes are excluded from the discriminants, so this does not constrain the parity of distinct qualifying discriminant primes. No Problem H or rank conclusion. The possible quotient m_6j/m_2j is an integer by odd multiplication, but its prime factors are not covered by this theorem unless they already divide m_2j D_2j. No claim about their interaction with earlier discriminants is made.
