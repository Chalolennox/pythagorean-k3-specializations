# Connected family of 32 arithmetic tori

For the sixteen owner-supplied prime residue rows in ARITHMETIC_SEED_TRANSPORT.md, search seeds 504m with m coprime to 6. Require identical active local lattices and singleton supports, solve simultaneous affine CRT constraints, and verify each local residue directly. Reject repeated translation classes modulo the common active lattice.

The supplied standalone Python script was rerun in the container and its stdout matched the supplied certificate transcript byte for byte. The repository reconstruction code/verify/verify_32_tori.py uses the same algorithm with a reformatted grid enumeration and an explicit final count assertion; that exact reformatted version has not separately been executed.

The 32 accepted multipliers are:
1, 5, 11, 25, 43, 55, 59, 61, 103, 127, 137, 157, 167, 193, 203, 215, 217, 227, 263, 275, 323, 329, 337, 353, 367, 371, 377, 397, 403, 437, 457, 461.

Common lattice basis (R,0),(-A,B):
R=89293690403146277207008248930360154325
A=57266895911890491006635872702305161050
B=17214925

The original translation for 2520 is reproduced exactly: (57734055708745284484672341832708165195,4886099). The last seed 232344 has certificate (66003040356639374442694692075427520597,12585714). The script prints all intermediate certificates.

Each certificate tau_n satisfies a_{p,n}(i,j)=a_{p,504}((i,j)+tau_n) for every selected prime. The 31 direct edges give 496 pairwise edges by subtraction of certificates. Distinctness modulo the common lattice establishes distinct collections of local prime labels because each active support is a singleton. Aggregate XOR distinctness is not separately established. All these tori are translation-equivalent, not 32 inequivalent isomorphism classes. The common lattice has odd index, so no subgroup of order 32 exists in its translation group. No complete parity claim, no independent recertification of the owner residue rows, and no consequence for Problem H is claimed. Earlier 128-torus and multiplier-cube numerical claims remain unverified.
