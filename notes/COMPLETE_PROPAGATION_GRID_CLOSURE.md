# Complete propagation-grid separation — closure (2026-11-25)

AI-authored proof and independent Python/SymPy verification; human review pending. Builds on NUMERATOR_DENOMINATOR_GRID_SEPARATION.md and paper F.20.

Let Q=jP on J:y²=x³−2x²+2x, P=(1,1), T=(0,0), x(jP)=m_j²/D_j² in lowest terms. Set h=H(1−x), N_j=D_j¹²h(x(jP)). Define C_j=m_6j/m_2j and B_j=D_6j/D_2j; both integral by formal group propagation (at odd primes; at 2 numerator odd and denominator divisibility follows from v2(D_n)=v2(n)). 

Theorem: gcd(m_6j D_6j, product_{k=1,2,3,6} N_kj)=1 for all j≥1. Equivalently gcd(product_{k=1,2,3,6} m_kj D_kj, product_{k=1,2,3,6} N_kj)=1, since each earlier numerator/denominator prime persists in or migrates to the final denominator or numerator. Indeed for p≥5 dividing any earlier coordinate numerator/denominator, [6/k] sends O or T to O or T. Primes 2,3 excluded by F.20.

Proof: at p≥5 dividing m_6j D_6j, 6Q reduces to O or T. If 2Q reduces to O or T, previous grid separation applies (including p=7,103, ord(P)=6,54). Otherwise 2Q has order 3 or 6, with triple O or T. Thus 3Q has order dividing 4, with double O or T. At O h homogenized is a unit; at T h(0)=-54; at other 2-torsion h mod (x²−2x+2)=-8; at order four with double T h mod (x²−2)=338x−484, resultant 5768, and 7,103 excluded by subgroup orders. Hence N_3j,N_6j are units.

For Q and 2Q use g3=3x⁴−8x³+12x²−4 and g6=x⁴−12x²+16x−12 (translation of nonzero 3-torsion by T, from x↦2/x). Set A=(x²−2)², B=4x(x²−2x+2). G3=3A⁴−8A³B+12A²B²−4B⁴; G6=A⁴−12A²B²+16AB³−12B⁴. At 2Q use g3,g6; at Q use G3,G6. Denominators are units in the case under consideration.

Exact absolute resultants with h:
g3: 2^6*19*797*7351
g6: 2^6*3^6*5273
G3: 2^24*3^6*19*797*4073*5273*7351*4573216980961
G6: 2^24*7^2*336737496728799825909507413201 (corrects earlier exponent 36).
G3=g3*g6*(x^8−8x^7+56x^6−112x^5+152x^4−224x^3+224x²−64x+16).

Every modular gcd for these resultants at p≥5 is linear. Table p, root, Legendre(x), Legendre(x³−2x²+2x):
7 5 -1 +1 (G6; distinct from earlier order-four root 4)
19 18 -1 -1
797 219 -1 -1
4073 344 +1 -1
5273 4145 -1 -1
7351 4295 -1 -1
4573216980961 2330679909894 -1 +1
336737496728799825909507413201 317738409857523285684352671772 -1 -1
All excluded by necessary square-coordinate and curve conditions. QED.

Primality: all factors below 2^64 pass deterministic SymPy isprime. For L=336737496728799825909507413201, L−1=2^4*5²*11*19*179*761*8573*3449170715522251, all factors verified prime (below 2^64); Lucas witness 15 verified: 15^(L−1)=1 mod L and gcd(15^((L−1)/q)−1,L)=1 for every prime q|L−1. Thus L is prime, not merely probable prime.

Independent verification executed in Python: exact SymPy polynomial factorization/resultants/modular gcds/Legendre symbols; exact Fraction group law for n=1..180, square coordinate checks, both quotient divisibilities and full product gcd=1 for j=1..30. All passed; largest N 121251 bits. No discriminant factorization. Earlier owner Magma log verifies initial grid separation, not these new quotient resultants. No new Magma run claimed.

Closure: direct shared-prime propagation between coordinate factors and discriminant factors is excluded on the entire {1,2,3,6} square. This does not exclude shared primes between discriminants themselves, additive relations, or parity correlations; no joint qualifying-prime parity restriction or Problem H conclusion follows. Stop extending this branch to larger multipliers absent a new mechanism. Human review pending.
