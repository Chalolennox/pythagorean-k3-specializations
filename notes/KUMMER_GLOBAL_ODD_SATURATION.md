# Global odd saturation over K — 2026-11-27

Owner-executed PARI/GP V4 certificate; AI-authored proof, independent human review pending. Supersedes the pending height step in KUMMER_ODD_SATURATION_10000.md.

Use the full x-height convention H(Q)=lim 4^(-n) h(x(2^n Q)), with absolute logarithmic Weil height h. The PARI V2 height 8.9387379895336553292778845054958966356 divided by degree 12 agrees numerically with Magma/Sage 0.744894832461138. No numerical height is required for the proof.

J: y²=x³−2x²+2x. A=(x²−2)², B=4x(x²−2x+2). Duplication x(2Q)=A/B. Exact identity:
(12x²−16x+16)A+(-3x³−2x²+10x+8)B=64.
At a finite place with |x|<=1, max(|A|,|B|)>=|64|; with |x|>1, |A|=|x|^4. At archimedean places with |x|<=2, the sum of absolute coefficient-polynomial values is at most 480, so max(|A|,|B|)>=64/480>=max(1,|x|)^4/120. For |x|>2, |A|>=|x|^4/4. Summing normalized local bounds gives h(x(2Q))>=4h(x(Q))−log(7680). The coefficient sums give the reverse bound h(x(2Q))<=4h(x(Q))+log20. Iteration for non-torsion Q gives h(x(Q))<=H(Q)+log(7680)/3<H(Q)+3 and H(Q)<=h(x(Q))+log20/3. For U, x(U) is integral and its monic sextic gives Cauchy root bound 190, hence H(U)<7.

## Uniform lower bound
F is the degree-12 field defined by f=y^12−66y^10−29922y^8+73214y^6−62559y^4+22032y²−3456. Owner PARI nfinit: signature [2,5], field discriminant −14970542793242443776 (curve discriminant −256).
At good primes the following degree-one places have reduction group orders dividing 60:
p=3: three places (ramification indices 6,3,3), N=6;
p=7: two places, N=12;
p=23: two places, N=20;
p=71: four places, N=60.
Thus for every non-torsion V, 60V belongs to the formal group at these eleven distinct places. Its x-coordinate has valuation <=−2 at each. No higher formal-group valuation estimate is needed.
D=3^6*7^4*23^4*71^8=316299002425639143508066329, and 2^88<D. Therefore h(x(60V))>=log(D)/12>88/18=44/9 (log 2>2/3).
Since h(x(60V))<3600H(V)+3, H(V)>17/32400.
If [l]V=U, l²<226800/17, so l<=115 and prime l<=113. Odd divisibility modulo torsion is equivalent to exact divisibility since the reported torsion order is 2.

Together with the prior finite exclusions and signed Galois/trace reduction (see KUMMER_ODD_SATURATION_10000.md), this proves saturation at all odd primes over K. The index in the saturation is a power of 2. This does not establish the full torsion-extension Kummer image or Problem H. Prior finite certificates and primitivity of P remain dependencies; the compact replay below does not reverify those.

The companion GP script is a compact reconstruction of the owner V4 search, using only m=60 and no formal-group depth increments. It is not independently executed.
