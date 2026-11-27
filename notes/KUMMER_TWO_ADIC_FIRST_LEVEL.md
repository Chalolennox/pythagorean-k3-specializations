# First-level 2-Kummer image

AI-authored proof, not human-reviewed. Depends on the owner-attested Magma square test and signed Galois computation. Let J: y²=x³−2x²+2x, h(x)=H(1−x), K the splitting field of the twelve points, M=<P,U_1,...,U_6>, L0=K(i,sqrt(2)), L∞=K(J[2^∞]). Write Y_j=x_j(x_j−1−i)(x_j−1+i), B_j=x_j−1−i.

## Owner certificate

Magma V2.30-1, seed 1779010529, output:
```
Polynomial: x^6 - 6*x^5 - 15*x^4 + 100*x^3 - 189*x^2 + 162*x - 54
Splitting field degree: 24
Absolute degree: 48
Final absolute degree: 96
Product identities: PASS
x_1 square over K(i,sqrt(2)): true
Square class certificate: (1 0 1 1 1 1)
CPU time: 277.220
TEST B: x_1 - 1 - i
The computation exceeded the time limit and so was terminated prematurely.
# 299.4s · Magma V2.30-1 | seed 1779010529
```
The tested base F is the sextic splitting field with i and sqrt(2) adjoined. The certificate means x_1 times Y_1 Y_3 Y_4 Y_5 Y_6 is a square in F. Since each Y_j is a square in K, x_1 is a square in L0, and by transitivity so is every x_j. No assertion about the identity of x_2 in the owner's root ordering is needed.

## Proof of rank three over L0

Full 2-descent uses the coordinates x and x−1−i. P=(1,1) has classes 1 and −i, both squares in L0. For every U_j the first coordinate is a square by the owner certificate. Because h(2−x)=h(x), the roots pair under x↦2−x. The identity B(2−x)=−(x−1+i), together with Y=x B(x)(x−1+i) and −1 square, shows that B(2−x) and B(x) have identical square classes. Thus at most three independent classes remain.

For the lower bound use p=125329, a completely split prime in K with p≡1 mod 8, hence split in L0. The roots in increasing order are 10263,37280,45627,79704,88051,115068. Taking the smaller square root of −1 modulo p, the quadratic character bits of B are (1,0,0,0,0,1), with 1 meaning nonsquare. The pairs are (10263,115068), (37280,88051), (45627,79704). The evaluation on the three paired classes is therefore a unit vector. Conjugating the prime by the Galois group of L0/Q gives all three unit evaluations: transitivity on pairs suffices, and conjugation of i replaces B by its equal square class. Any square-class relation must vanish on all three evaluations. Hence rank exactly three and [L0(1/2 M):L0]=8. This argument does not require consistent arbitrary root sorting at different primes.

Since L0⊂L∞ by the Weil pairing, the mod-2 translation image over L∞ has dimension at most three, and its index in Z_2^14 is divisible by 2^11=2048. The exact dimension is 3−log2([L0(1/2 M)∩L∞:L0]). This intersection, higher division levels and the local weighted correction factor remain open. The index is not the correction factor. No claim about C or Problem H.

The finite-field evaluation was computed in JavaScript in the research conversation; a compact Magma verifier is supplied separately and is not claimed to have been executed.
