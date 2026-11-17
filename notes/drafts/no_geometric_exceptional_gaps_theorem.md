<!-- Provenance: pasted into the chat by the repository owner on 17 November 2026 (message "add this result to that too"), origin not stated. Reviewed in notes/REVIEW_2026-11-17_gap_three_dossier.md, section 5; the premises are checked in code/verify_gap_three.py (checks 9 and 10).
     The text below the line is unmodified. -->

---

Theorem: no geometric exceptional gaps

Let C:y²=x³−2x²+2x, P=(1,1), and let D be the divisor defined by H(1−x)=0, H(t)=t⁶−30t⁴−24t²−1. Then D∩τ_{−kP}(D)=∅ for every integer k≠0.

The proof uses two verified facts:

1. The degree-12 polynomial defining the points of D is irreducible over ℚ. Thus the 12 points form one Galois orbit.
2. P has infinite order, as demonstrated by the nonintegral x-coordinate of 2P.

Any nonempty intersection of D with a rational translate would be Galois-stable. Because D is one Galois orbit, that intersection would contain all of D. Translation by kP would therefore preserve a finite set, impossible for a nontorsion point. This establishes the theorem.

What the theorem gives us:

For every fixed L, there is a finite exceptional-prime set E_L such that, outside it, I_{p,ε}(n)I_{p,ε}(n+k)=0 simultaneously for all 1≤k≤L. This is the foundation of the arithmetic sieve you proposed. However, the exceptional set depends on L. We have not proved that there is a single finite set of primes working for every gap.

A stronger quantitative consequence:

Because D consists of exactly 12 geometric points, the qualifying residue set contains at most 12 elements: |R_{p,ε}|≤12 at every good prime. Therefore, for every p with m_p=ord(P mod p)>12, δ_{p,ε}=|R_{p,ε}|/m_p≤12/m_p.

Moreover, for every fixed M, only finitely many primes can satisfy m_p≤M: otherwise one of the finitely many nonzero points P,2P,…,MP would reduce to the identity modulo infinitely many primes. Consequently, δ_{p,ε}→0 (p→∞). This is unconditional.
