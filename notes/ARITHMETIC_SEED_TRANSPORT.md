# Arithmetic seed transport and simultaneous translation

For the fixed 16 primes of PR92, define O_p(n)={n2^i3^j mod d_p}, and R_p the qualifying residues. The map x -> mx sends O_p(n) onto O_p(mn), commutes with multiplication by 2 and 3, and pulls the destination label back to the indicator of {x: mx in R_p}. It does not generally preserve source labels. The maps for 5 and 7 commute, giving the square of seeds 72,360,504,2520. Retaining the entire source orbit and all qualifying residues (including inactive ones) suffices to transport supports without elliptic curve recomputation.

## Executed orbit transport

Columns are qualifying residues for seeds 72,360,504,2520 respectively; dash means empty.
|p|72|360|504|2520|
|---|---|---|---|---|
|2131|388|388|643|643|
|5779|1617|1286|1617|1286|
|6907|6|6|6|6|
|10321|639|1950|1950|639|
|12907|-|810|-|-|
|13763|240|240|6719|6719|
|18797|6804|6804|6804|6804|
|23747|3037|8746|8746|3037|
|40841|5740|4507|5740|4507|
|46933|20620|20620|1344|1344|
|47657|6858|5069|6858|5069|
|47701|14064|9644|14064|9644|
|52883|11592|14751|14751|11592|
|54517|5520|21736|5520|21736|
|72883|27086|27086|9393|9393|
|77347|32998|-|-|-|

Only local orbit sizes at 12907 (172 -> 43 under 5) and 46933 (2514 -> 419 under 7) change. The destination singleton pulls back to four or six points respectively. Active counts 15,15,14,14.

## Exact translation theorem

For seeds 504 and 2520, the fourteen active local lattices are identical and both remaining supports empty. For each active prime, choose representatives A,B of the singleton positions for 504 and 2520. The translation constraint is (u,v) in A-B+L_p. Exact affine CRT intersection in JavaScript succeeded for all fourteen primes, with certificate
u=57734055708745284484672341832708165195, v=4886099.
The solution lattice has basis (89293690403146277207008248930360154325,0),(-57266895911890491006635872702305161050,17214925).
Thus a_{p,2520}(i,j)=a_{p,504}(i+u,j+v) for every selected prime and vertex. XOR preserves the identity. Translation preserves uniform counting on a common finite period quotient, hence all finite pattern frequencies agree, not only the sixteen elementary square frequencies. In particular the Walsh vectors are exactly equal. This conclusion does not require trusting rounded numerical Walsh results.

Reproduction script code/verify/pr92_seed_translation.py reconstructs source orbits, checks commuting images, solves the affine CRT constraints, and independently checks the explicit translation on every local orbit residue. It is a standalone Python reconstruction of the executed JavaScript calculation; the Python version itself has not been run in this turn. Earlier Walsh results are recorded separately in DE_BRUIJN_WALSH_DISTRIBUTION.md. No claim that the aggregate Walsh vector alone suffices to transport labels, or that the complete infinite-prime labeling has this symmetry. Human review pending.
