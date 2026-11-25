# De Bruijn arithmetic common cover

25 November 2026. Companion to ARITHMETIC_TORUS_COVERING.md. Owner Magma output, V2.30-1, seed 1778804089, CPU 2.740 s. Proofs below derived with a language model; human review pending.

## Reference torus

On Z/4 x Z/4 the binary rows are 1110,1101,0100,1000. With code 8a+4b+2c+d for a wrapped elementary square, the rows of codes are (15,14,9,7), (13,10,4,12), (6,8,0,1), (11,3,2,5). All 16 codes occur once, eight vertices are marked, and V-E+F=16-32+16=0. This is a combinatorial reference, not a hypothesis about the rational orbit.

For arithmetic lattice L and reference lattice L4=4Z^2, the common cover is Z^2/(L intersect L4). Both quotient maps are surjective with constant fiber sizes. If C=sum_p |S_p|/|G_p|, arithmetic marked density is at most C, zero-tile density at least 1-4C, vertex disagreement with any translated reference at least 1/2-C, and tile disagreement and total variation from uniform at least 1-4C-1/16 (truncate negative bounds at zero). These follow by union bounds and comparison of marginals. Horizontal and vertical mean sign products are at least 1-4C; rectangle mean product at least 1-8C.

## Owner computation

Same 16 primes as ARITHMETIC_TORUS_COVERING.md. Seeds 72,360,2520; active counts 15,15,14; common-cover degrees over arithmetic torus 2,8,16. C respectively 0.0107838811974069, 0.0336780314980923, 0.0124110799153279. Lower zero-tile densities 0.956864475210373, 0.865287874007630, 0.950355680338689. Lower tile disagreement 0.894364475210373, 0.802787874007630, 0.887855680338689. Observed 64x64 window tile disagreement 0.939453125, 0.93603515625, 0.94091796875; these are not global densities. Every active local support is singleton and its four shifted support cosets are distinct. Local code distribution for group size M is mass 1-4/M at 0 and 1/M at each of 1,2,4,8, zero elsewhere. This is verified for the tested seeds, not a universal theorem.

Exact global distribution deferred due to large dependency components (seed 72 largest size 4452550043662125633089736875). No independence assumed within those components. Raw owner transcript and script not archived here.

## All configurations realized (finite-prime theorem)

For seed 72 the four singleton dependency components p=5779,10321,23747,47657 have group sizes 1451,431,5891,5963. The dependency graph joins local groups whose orders have gcd greater than one. The four listed components are isolated, so their orders are pairwise coprime and coprime to the order of the joint quotient of the remaining groups (the latter divides the product of remaining local orders). The joint quotient projects surjectively to each of these five factors. Its order is divisible by each factor order, hence by their product, and it is a subgroup of their product. Thus the joint quotient is the full product.

Each of the four isolated components can realize zero or any one of the four unit codes. For any fixed code from the remaining factors and any target code, assign the required XOR difference to the four isolated components, one component per bit, using zero when that bit is absent. Surjectivity realizes all assignments simultaneously. Consequently every one of the 16 codes has strictly positive uniform mass on the finite arithmetic torus. This proves existence without enumerating the large component. It also applies to the other two tested seeds, which retain the same four isolated components and local unit-code distributions. No assertion about full-prime parity follows.

## Exact reference disagreement for seed 2520

The arithmetic quotient (including inactive local periods) has odd order 5221814670545711800124268461600280510118142223125. Its common cover with the reference has order 83549034728731388801988295385604488161890275570000, exactly 16 times the arithmetic order. The joint projection to the arithmetic quotient and Z^2/4Z^2 is therefore bijective (alternatively use coprime orders and surjectivity). Uniform counting gives independence of the arithmetic and reference coordinates. The reference vertex label is uniform on {0,1}, and its tile code uniform on all 16 codes. Conditional on any arithmetic vertex label or tile code, agreement probabilities are exactly 1/2 and 1/16 respectively. Hence exact vertex disagreement 1/2 and tile disagreement 15/16, for every reference translation, independent of the unknown arithmetic distribution.

## Next computational option and limitation

Sparse coset intersection via generalized CRT and character expansion can replace exhaustive vertex enumeration. For each of the 16 binary characters of the four-bit code, expand the product of local signs as products of (1-2 indicator of a shifted singleton coset), combining mutually exclusive local events before expansion. Each compatible intersection is a coset of the intersection lattice, with density reciprocal to its index; incompatible intersections have density zero. Walsh inversion recovers exact code masses. This algorithm has not been executed here; naive expansion can be expensive.

All results concern finite prime truncations. The complete rational orbit need not be periodic on the common cover, and the de Bruijn reference is not a required arithmetic labeling. No tail bound or consequence for Problem H is claimed.
