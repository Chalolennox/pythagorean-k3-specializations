# Exact Walsh distributions on arithmetic tori

25 November 2026. Companion to DE_BRUIJN_ARITHMETIC_COVER.md. Python exact rational calculation rerun successfully using the owner Magma residues. Human review pending.

For each active prime the singleton support and its four shifts are distinct affine lattice cosets C[p,l]. For character w in F2^4 the local factor is 1-2 sum_{l:w_l=1} 1_C[p,l]. Expand the product over primes, intersecting affine cosets and collecting integer coefficients. An empty intersection contributes zero; a nonempty coset contributes reciprocal lattice index. This gives exact Walsh coefficients W(w). Invert by mu(k)=sum_w (-1)^(w dot k) W(w)/16. Coprime dependency components factor as proved in the companion note.

## Affine intersection algorithm

Represent a coset by (r,a,b,x,y), lattice generators (r,0),(-a,b), representative (x,y). Membership means j=y mod b and i=x-a*(j-y)/b mod r. For a second coset (s,c,d,u,v), solve j=Y mod L=lcm(b,d) by generalized CRT; incompatible means empty. Set X=x-a*(Y-y)/b, U=u-c*(Y-v)/d, g=gcd(r,s), h=a*L/b-c*L/d. Solve h*k=X-U mod g; incompatible means empty. Replace Y by Y+L*k, set B=L*g/gcd(h,g), R=lcm(r,s). Solve the horizontal congruences at this Y by CRT for representative Xnew. Solve A=a*B/b mod r, A=c*B/d mod s by CRT. The resulting coset is (R,A,B,Xnew,Y). Its density is 1/(R*B). This proves the algorithm without assuming independence within components.

## Executed results

Rows below are codes 0 through 15; columns seeds 72,360,2520. Decimal renderings of exact rational computations, not empirical frequencies.

|code|72|360|2520|
|---|---:|---:|---:|
|0|0.9578641715697435|0.8709411096498461|0.9516713474614166|
|1|0.01038575514539767|0.03143230502082468|0.011887506359307683|
|2|0.01038577744530311|0.03143230502082468|0.011887506359307683|
|3|9.823136707476142e-5|0.0005502515587673437|0.0001289377693747694|
|4|0.010385791414751063|0.03143230502082468|0.011887492655980101|
|5|9.829048910951366e-5|0.0005503024749547276|0.00012895147270235087|
|6|9.823504415016188e-5|0.0005502515587673437|0.0001290071637451867|
|7|7.983289757924088e-7|6.997304509976834e-6|1.2130120776319094e-6|
|8|0.010385757001302783|0.03143230502082468|0.011887492655980101|
|9|9.825703913374678e-5|0.0005502515587673437|0.0001290071637451867|
|10|9.830260265235461e-5|0.0005503024749547276|0.00012895147270235087|
|11|7.986338976466405e-7|6.997304509976834e-6|1.2130120776319094e-6|
|12|9.821554172169178e-5|0.0005502515587673437|0.00012896517602993237|
|13|8.126033456019354e-7|6.997304509976834e-6|1.1993087500504337e-6|
|14|8.001848809067567e-7|6.997304509976834e-6|1.1993087500504337e-6|
|15|5.588559722567882e-9|6.986383647333731e-8|9.648052699400605e-9|

Exact assertions sum(mu)=1 and min(mu)>0 passed for each seed. Odd marginal densities 0.010682949195494455, 0.0331041723906805, 0.012278037746088004. Horizontal correlations 0.9576675388920539, 0.8698405745637731, 0.9514133427819789; vertical 0.9576678312579847, 0.8698407782285226, 0.9514133427819789; rectangle 0.9169074184842908, 0.7484855813973227, 0.9048903546555381.

## Tail complement theorem

If H fails in the sense of eventual all-odd complete parity on the original orbit, every sufficiently late multiplication square has complete code 15. Thus its unselected-prime code equals 15 XOR selected-prime code, or 15-k. Only finitely many grid vertices lie below the eventual threshold. Consequently rectangular limiting tail frequencies exist under this hypothesis and equal mu_tail(k)=mu_selected(15-k). Tail odd marginal equals one minus selected odd marginal (approximately 98.93170508%, 96.68958276%, 98.77219623% for the three seeds). In particular seed 72 requires tail code 15 density 0.9578641715697435. Any independently established incompatible tail frequency would refute eventual all-oddness. This is a necessary condition, not an independent tail estimate. No proof of H.

The implementation was rerun; the earlier reported randomized intersection tests were not rerun in this commit. Decimal output is rounded. No full-prime distribution or arithmetic realization of the de Bruijn reference is asserted.
