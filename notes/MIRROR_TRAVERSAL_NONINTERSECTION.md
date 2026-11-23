# Mirror nonintersection in the rational circle traversal

Status: algebraic argument; computational checks supplied by Magma V2.30-1 for gaps 1–12. This is a research note and a place to collect further results, not a claim about global root-number distribution.

## Setup

Let J/Q be y^2=x^3-2x^2+2x, P=(1,1), T=(0,0), and R=P+T. On the quotient J/{±1} define t(Q)=1-x(Q), extended to P^1 at the point at infinity. The mirror involution is M(t)=(t+1)/(t-1). Translation by T has x(Q+T)=2/x(Q), hence M(t(Q))=t(Q+T), including the projective extensions.

For k≠0, let G_k(a,b)=0 denote the symmetric projected correspondence of translation by kR. The explicit formula, writing u=x(kR), X=1-a and Z=1-b, is

G_k(a,b)=(X-u)^2 Z^2 + (-2u^2 X-2uX^2+8uX-4u-4X)Z +u^2X^2-4uX+4.

This is the general-gap correspondence already discussed in Appendix F.57 of paper/paper.md.

## Proposition: no rational mirror-paired parameter

For any nonzero integer k there is no t in P^1(Q) for which G_k(t,M(t))=0.

Proof. Choose Q over t (over an algebraic closure). The condition is x(Q+kR)=x(Q+T), so either kR=T or 2Q=-kR-T. The first is impossible since R has infinite order. If t is rational, x(Q) is rational; we must show the second equation has no solution even with rational x(Q).

If t(Q) is rational, x(Q) is rational, so for every σ in Gal(Qbar/Q), σ(Q)=Q or -Q. In the second case, 2Q=-kR-T=:C is a non-torsion rational point (as R has infinite order). Applying σ gives 2σ(Q)=C. If σ(Q)=-Q, then C=-C, a contradiction. Therefore every conjugate fixes Q: Q is rational. (This elementary Galois argument also applies to points with rational x and non-torsion rational doubles.)

If k=2m, 2(Q+mR)=T. But a rational point S with 2S=T would satisfy x(S+T)=x(S), hence x(S)^2=2, impossible over Q.

If k=2m+1, -kR-T=-kP-2(m+1)T=-kP, so after adding mP to Q one obtains 2(Q+mP)=-P. The duplication equation x(2S)=1 has numerator (x^2-4x+2)(x^2+2), with no rational roots. Thus P is not twice a rational point.

Both parities are excluded, including projective boundary parameters. This proves the proposition for rational *parameters*, not merely rational elliptic points.

## Verified computations

Magma V2.30-1 checked the exact torsion-translation identity and the mirror-polynomial rational roots for k=1,...,12. No rational affine mirror-pair roots were found. For odd k=1,3,5,7,9,11 the quartic factors as two quadratics over Q; for even k=2,4,6,8,10,12 it was irreducible. These are finite observations, not an all-k factorization theorem.

The boundary t=1 gives a repeated projected neighbor for every k, since it corresponds to T=-T. Fixed-point equations G_k(t,t)=0 have rational roots at even gaps in the tested range; the corresponding group-law argument extends to rational parameters by the same Galois observation when the relevant doubled point is non-torsion.

## Scope and further collection

The reflection M(t) is not the sign reflection t -> 2-t (which exchanges 1-x and 1+x); keep these two involutions distinct. Mirror nonintersection does not imply disjointness of full orbit images, nor global root-number parity independence. Please append new exact results, counterexamples, proof corrections and scripts in this PR discussion before promoting claims to the paper.
