# Quarter-divisibility of P over the 2-power torsion field

AI-authored symbolic proof, human review pending. Let J: y²=x³−2x²+2x, P=(1,1), T=(0,0), T_n=Q(J[n]), L_inf=K Q(J[2^infty]). Builds on KUMMER_TWO_ADIC_INTERSECTION.md.

Put a=sqrt(2). The point R=(2−a,2−2a) satisfies the curve equation (both sides equal 12−8a). Its doubling slope is 1−a; the doubling formulas give x(2R)=1 and y(2R)=1. Thus 2R=P. (The positive ordinate doubles to −P.)

The full 2-descent coordinates of R are d1=2−a and d2=1−a−i. Both are squares in T_16:
* d1=(zeta_16^3+zeta_16^(-3))² for zeta_16=exp(2 pi i/16); the Weil pairing supplies zeta_16.
* Choose S with x(S)=a and 2S=T, possible by the duplication identity x(2S)=(x(S)^2−2)^2/(4y(S)^2). Then S belongs to J[4], and any half V belongs to J[8]. The full 2-descent criterion implies x(S)−(1−i)=a−1+i is square in T_8. Its negative d2 is also square there because i is present.

Hence R is twice a point over T_16 and P belongs to 4J(T_16). No computational certificate is needed.

For H=H_2 in Lambda=Z_2^14, with the first two coordinates corresponding to P, the projection to those coordinates vanishes mod 4. From the exact first-level dimension 2, |H mod 4| <= 2^(2+12)=16384. Thus 16384 divides [Lambda:H], and 2 Lambda is not contained in H. Equality of the index is not established.

## Roadmap
1. First-level image: exact dimension 2 (completed).
2. Proposed maximal second layer: disproved by the P component (completed).
3. Determine the exact P projection, starting with eighth-divisibility over the torsion field.
4. Determine second-layer geometric translation constraints, including relations between opposite root pairs; use finite certificates and Galois action, not odd-characteristic sign isolation.
5. Determine higher layers until a full congruence submodule is certified; compute exact index.
6. Evaluate the index-weighted local statistic, including eligibility and cross-prime entanglement. Index alone is not the correction factor.
7. Establish exceptional-prime exhaustiveness and uniform tail control before claiming a global constant C. Problem H remains separate and open.
