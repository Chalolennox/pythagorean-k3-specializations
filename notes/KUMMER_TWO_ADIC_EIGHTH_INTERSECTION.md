# Eighth division of P: exact exclusions and stabilization criterion

J: y^2=x^3-2x^2+2x, P=(1,1). Write T_n=Q(J[n]), T_infty=union T_(2^n). Previous quarter-division certificate gives B=Q(sqrt(2),i,S) inside T_16, where 4S=P.

## Owner Magma run (2026-11-27)
V2 output: base degree 4, quarter polynomial V^4+(4a-8)V^3+(-8a+12)V^2+(8a-16)V+4, a^2=2; irreducible degree 4. Quarter point verified, B degree 16. Classes d1=x(S), d2=x(S)-1-i, d3=d1*d2 all nonsquare. Each quadratic extension has absolute degree 32. Eighth-division quartic irreducible; independent factorization check PASS. CPU 0.120s, Magma V2.30-1, seed 1778929625. Hence N=B(8^{-1}P) is biquadratic over B.

## Exact Frobenius exclusion
p=557057, i=33793. Independent halving computations give paths from 0 and 1+i:
0,430743,308029,34137,522809,553857;
33794,205976,111554,384197,97345,52490.
These certify full J[64] rational. All 16 quarter-point x coordinates have character vector (+1,-1,-1) for d1,d2,d3. See code/verify/pr92_eighth_division_witness.py. The modular calculations were independently replayed using integer arithmetic; the newly committed standalone Python replay itself has not been executed in this session. Thus d2 and d3 cannot be squares over T_64 and N intersect T_64 is contained in B(sqrt(d1)). At p=1251329 all three characters were +1 on all 16 quarter coordinates. No containment follows from this positive test.

## Finite stabilization criterion (new conditional reduction)
Let G be the image on the 2-adic Tate module and G(64) the kernel of reduction modulo 64. If G(64) maps onto the full four-dimensional space M_2(F_2) in the kernel of GL_2(Z/128) -> GL_2(Z/64), then G(64)=1+64 M_2(Z_2). Indeed, squaring 1+2^k A modulo 2^(k+2) gives 1+2^(k+1) A for k>=2. Surjectivity propagates to every successive layer, and closedness gives equality. Moreover the square map from 1+64 M_2(Z_2) onto 1+128 M_2(Z_2) is surjective (binomial square-root series, or iterative lifting). Every elementary abelian 2-quotient of G(64) therefore factors through G(64)/G(128). Consequently every elementary abelian 2-extension of T_64 inside T_infty lies in T_128. Since N T_64/T_64 is elementary abelian, N intersect T_infty = N intersect T_128 under this hypothesis.

The existing repository brute-force crosscheck reports p=557057 has torsion level 7 and P divisibility depth 2. To extend the explicit certificate to T_128, append one more halving step to both paths. With that verified, d2,d3 are excluded at T_128 as well. Under the full-kernel hypothesis they are then excluded at infinite level. This does not prove d1 containment, nor the exact higher translation lattice index: even a one-dimensional mod-8 image need not imply index 32 without a higher-layer lifting certificate.

## Open tasks
1. Prove full congruence kernel hypothesis (four independent mod-128 kernel matrices suffice).
2. Prove d1 square in T_64 or T_128, by exact field or group certificate.
3. Establish higher translation lifting; do not infer exact index from first-level rank alone.
No claim about Problem H parity or the compositum with the signed geometric field K follows here.
